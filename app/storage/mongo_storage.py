from typing import Any
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from starlette.datastructures import URL

from pymongo import MongoClient, database, collection, ReturnDocument
from app.exceptions.general_exceptions import (
    ImmutableFieldError,
    NoUniqueElement,
    ResourceNotFound,
)
from app.http.hateoas import HrefProvider

from app.models.users import User

from ..config import DbConfig
from ..models.general import PaginatedResponse, Test
from ..models.products import Product, ProductListCollection
from ..models.customers import Customer, CustomerPagination


class Paginator:
    def __init__(
        self,
        collection: collection.Collection,
        page: int,
        per_page: int,
        sort: tuple[str, int],
        filters: dict[str, Any] = {}
    ):
        self.collection = collection
        self.page = page
        self.per_page = per_page
        self.filters = filters
        self.skip = per_page * (page - 1)
        self.sort = sort

    def __get_url(self, params: dict) -> URL:
        return HrefProvider.get_url_with_params(params)

    def __get_data(self):
        return self.collection.find(self.filters).sort(*self.sort).skip(self.skip).limit(self.per_page)

    def __get_count(self) -> int:
        self.count = self.collection.count_documents(self.filters)
        return self.count

    def __get_total_pages(self) -> int:
        return (
            self.count // self.per_page + 1
            if self.count % self.per_page
            else self.count // self.per_page
        )

    def __get_next_page(self) -> str | None:
        if self.page < self.__get_total_pages():
            url = self.__get_url({"page": self.page + 1})
            return str(url)
        else:
            return None

    def __get_previous_page(self) -> str | None:
        if self.page > 1:
            url = self.__get_url({"page": self.page - 1})
            return str(url)
        else:
            return None

    def get_pagination(self) -> PaginatedResponse:
        return PaginatedResponse.model_validate(
            {
                "data": self.__get_data(),
                "count": self.__get_count(),
                "total_pages": self.__get_total_pages(),
                "next_page": self.__get_next_page(),
                "previous_page": self.__get_previous_page(),
            }
        )


class MongoStorage:
    def __init__(self, dbConfig: DbConfig) -> None:
        self.config = dbConfig
        self.client: MongoClient[dict[str, Any]] = MongoClient(
            dbConfig.db_username, dbConfig.port
        )
        self.db: database.Database[dict[str, Any]] = self.client[dbConfig.db_name]
        self.users_collection: collection.Collection = self.db.users
        self.health_collection: collection.Collection = self.db.health
        self.products_collection: collection.Collection = self.db.products
        self.customers_collection: collection.Collection = self.db.customers

    def __validate_personal_id(self, id: str) -> bool:
        all_ids = [
            customer["personal_id"]
            for customer in self.customers_collection.find(
                {}, {"_id": 0, "personal_id": 1}
            )
        ]

        if id in all_ids:
            return False

        return True

    def __paginate(
        self,
        collection: collection.Collection,
        page: int,
        per_page: int,
        filters: dict[str, Any] = {},
        sort_by: str | None = None,
        direction: int | None = None
    ) -> PaginatedResponse:
        sort_param = (sort_by or "_id", direction or 1)
        paginator = Paginator(collection, page, per_page, sort_param, filters)
        return paginator.get_pagination()

    def test_database(self) -> list[Test]:
        test: list[Test] = list(self.health_collection.find({}))
        return test

    def get_products_list(self) -> ProductListCollection:
        products: list[Product] = [
            Product.model_validate(product)
            for product in self.products_collection.find({})
        ]
        return ProductListCollection(data=products)

    def get_product_by_id(self, id: int) -> Product:
        product: Product | None = self.products_collection.find_one({"id": id})

        if not product:
            raise ResourceNotFound

        return Product.model_validate(product)

    def get_customers_list(self, per_page: int, page: int, sort_by: str | None = None, direction: int | None = None, search: str = '') -> CustomerPagination:
        filters = { "$or": [ {"family_name": {"$regex": search}}, {"middle_name": {"$regex": search}}, {"surname": {"$regex": search}}, {'additional_surname': {"$regex": search} } ]} if search else {} 
        response = self.__paginate(self.customers_collection, page, per_page, sort_by=sort_by, direction=direction, filters=filters)

        parsed_response = CustomerPagination.model_validate(response.model_dump())

        return parsed_response

    def get_customer_by_id(self, id: int) -> Customer:
        customer = self.customers_collection.find_one({"id": id})

        if not customer:
            raise ResourceNotFound

        return Customer.model_validate(customer)

    def create_customer(self, customer: Customer) -> Customer:
        is_personal_id_valid = self.__validate_personal_id(customer.personal_id)

        if not is_personal_id_valid:
            raise NoUniqueElement

        insert_response = self.customers_collection.insert_one(
            jsonable_encoder(customer)
        )
        new_customer = self.customers_collection.find_one(
            {"_id": insert_response.inserted_id}
        )

        return Customer.model_validate(new_customer)

    def update_customer(self, id: int, customer: Customer) -> Customer:
        current_customer = self.get_customer_by_id(id)

        if not customer:
            raise ResourceNotFound

        if customer.personal_id != current_customer.personal_id:
            is_personal_id_valid = self.__validate_personal_id(customer.personal_id)

            if not is_personal_id_valid:
                raise NoUniqueElement

        if current_customer.id != customer.id:
            raise ImmutableFieldError("id")

        updated_customer = self.customers_collection.find_one_and_update(
            {"id": id},
            {"$set": jsonable_encoder(customer)},
            return_document=ReturnDocument.AFTER,
        )
        return Customer.model_validate(updated_customer)

    def delete_customer(self, id: int) -> None:
        removed_article = self.customers_collection.find_one_and_delete({"id": id})

        if not removed_article:
            raise ResourceNotFound

    def get_user(self, id: int | None = None, mail: EmailStr | None = None) -> User:
        if not id and not mail:
            raise ValueError("Either 'id' or 'mail' parameter must be provided.")
        if id and mail:
            raise ValueError(
                "Only one of 'id' or 'mail' parameters should be provided."
            )

        user = self.users_collection.find_one({"$or": [{"id": id}, {"mail": mail}]})

        if not user:
            raise ResourceNotFound

        return User.model_validate(user)
