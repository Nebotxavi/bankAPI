from pydantic import EmailStr
from starlette.datastructures import URL
from typing import Dict

from app.http.hateoas import HrefProvider
from app.models.users import User

from ..config import DbConfig
from ..models.products import Product, ProductListCollection
from ..models.customers import Customer, CustomerPagination
from ..models.users import User
from ..models.general import Test, PaginatedResponse
from ..exceptions.general_exceptions import (
    ImmutableFieldError,
    NoUniqueElement,
    ResourceNotFound,
)
from ..data.customers import mock_parsed_customers
from ..data.products import mock_parsed_products
from ..data.users import mock_parsed_users


class Paginator:
    def __init__(self, dataset_list: list, page: int, per_page: int):
        self.dataset_list = dataset_list
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page
        self.count = len(dataset_list)

        # self.total_pages = 0

    def _get_url(self, params: Dict) -> URL:
        return HrefProvider.get_url_with_params(params)

    def __get_paginated_dataset(self) -> list:
        return self.dataset_list[self.offset : self.offset + self.per_page]

    def __get_total_pages(self) -> int:
        return (
            self.count // self.per_page + 1
            if self.count % self.per_page
            else self.count // self.per_page
        )

    def __get_next_page(self) -> str | None:
        if self.page < self.__get_total_pages():
            url = self._get_url({"page": self.page + 1})
            return str(url)
        else:
            return None

    def __get_previous_page(self) -> str | None:
        if self.page > 1:
            url = self._get_url({"page": self.page - 1})
            return str(url)
        else:
            return None

    def get_pagination(self) -> PaginatedResponse:
        data = self.__get_paginated_dataset()
        total_pages: int = self.__get_total_pages()
        next_page: str | None = self.__get_next_page()
        previous_page: str | None = self.__get_previous_page()

        return PaginatedResponse.model_validate(
            {
                "data": data,
                "count": self.count,
                "total_pages": total_pages,
                "next_page": next_page,
                "previous_page": previous_page,
            }
        )


class StateStorage:
    def __init__(self, dbConfig: DbConfig) -> None:
        self.test_list = [Test(name="Pepi", test=77), Test(name="SuperTest", test=99)]

        self.users_list: list[User] = [
            User.model_validate(user.model_dump()) for user in mock_parsed_users
        ]

        self.products_list: list[Product] = [
            Product.model_validate(product.model_dump())
            for product in mock_parsed_products
        ]

        self.customers_list: list[Customer] = [
            Customer.model_validate(customer.model_dump())
            for customer in mock_parsed_customers
        ]

    def __paginate(
        self, dataset_list: list, page: int, per_page: int
    ) -> PaginatedResponse:
        paginator = Paginator(dataset_list, page, per_page)
        return paginator.get_pagination()

    def __validate_personal_id(self, id: str) -> bool:
        all_ids = [customer.personal_id for customer in self.customers_list]

        if id in all_ids:
            return False

        return True

    # TODO: to be removed
    def test_database(self) -> list[Test]:
        return self.test_list

    def get_products_list(self) -> ProductListCollection:
        products = self.products_list
        return ProductListCollection(data=products)

    def get_product_by_id(self, id: int) -> Product:
        product = next((x for x in self.products_list if x.id == id), None)

        if not product:
            raise ResourceNotFound

        return Product.model_validate(product)

    def get_customers_list(self, per_page: int, page: int, sort: str | None = None, direction: int | None = None) -> CustomerPagination:
        dataset: list[Customer] = self.customers_list
        response = self.__paginate(dataset, page, per_page)

        parsed_response = CustomerPagination.model_validate(response.model_dump())

        return parsed_response

    def get_customer_by_id(self, id: int) -> Customer:
        customer = next((x for x in self.customers_list if x.id == id), None)

        if not customer:
            raise ResourceNotFound

        return Customer.model_validate(customer)

    def create_customer(self, customer: Customer) -> Customer:
        is_personal_id_valid = self.__validate_personal_id(customer.personal_id)

        if not is_personal_id_valid:
            raise NoUniqueElement

        self.customers_list.append(customer)

        return Customer.model_validate(customer)

    def update_customer(self, id: int, customer: Customer) -> Customer:
        customer_index = next(
            (
                ind
                for ind, customer in enumerate(self.customers_list)
                if customer.id == id
            ),
            None,
        )

        if customer_index == None:
            raise ResourceNotFound

        current_customer = self.customers_list[customer_index]

        if customer.personal_id != current_customer.personal_id:
            is_personal_id_valid = self.__validate_personal_id(customer.personal_id)

            if not is_personal_id_valid:
                raise NoUniqueElement

        if current_customer.id != customer.id:
            raise ImmutableFieldError("id")

        validated_customer = Customer.model_validate(customer)

        self.customers_list[customer_index] = validated_customer

        return self.customers_list[customer_index]

    def delete_customer(self, id: int) -> None:
        customer_index = next(
            (
                ind
                for ind, customer in enumerate(self.customers_list)
                if customer.id == id
            ),
            None,
        )

        if customer_index == None:
            raise ResourceNotFound

        del self.customers_list[customer_index]

    def get_user(self, id: int | None = None, mail: EmailStr | None = None) -> User:
        if not id and not mail:
            raise ValueError("Either 'id' or 'mail' parameter must be provided.")
        if id and mail:
            raise ValueError(
                "Only one of 'id' or 'mail' parameters should be provided."
            )

        user = next(
            (user for user in self.users_list if user.id == id or user.mail == mail),
            None,
        )

        if not user:
            raise ResourceNotFound

        return user
