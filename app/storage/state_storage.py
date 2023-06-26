from fastapi import HTTPException, status
from typing import List, Dict, Any, TypeVar, Generic
import uuid

from ..config import DbConfig
from ..models.products import ProductType, Product, ProductList
from ..models.customers import Customer, CustomerIn, CustomerList
from ..models.general import Test, PaginatedObject
from ..exceptions.general_exceptions import noUniqueElement, resourceNotFound
from ..data.customers import mock_customers_list
from ..middleware.middleware import request_object

T = TypeVar('T')


class Paginator(Generic[T]):

    def __init__(self, dataset_list: List[T], page: int, per_page: int):
        self.dataset_list = dataset_list
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page
        self.count = len(dataset_list)
        self.request = request_object.get()

        self.total_pages = 0

    def _get_url(self, params):
        return self.request.url.include_query_params(**params)

    def _get_paginated_dataset(self) -> List[T]:
        return self.dataset_list[self.offset: self.offset + self.per_page]

    def _get_total_pages(self) -> int:
        total_pages = self.count // self.per_page + \
            1 if self.count % self.per_page else self.count // self.per_page
        self.total_pages = total_pages
        return self.total_pages

    def _get_next_page(self) -> str | None:
        if self.page < self.total_pages:
            url = self._get_url({'page': self.page + 1})
            return str(url)
        else:
            return None

    def _get_previous_page(self) -> str | None:
        if self.page > 1:
            url = self._get_url({'page': self.page - 1})
            return str(url)
        else:
            return None

    def get_pagination(self) -> PaginatedObject:
        data = self._get_paginated_dataset()
        total_pages: int = self._get_total_pages()
        next_page: str | None = self._get_next_page()
        previous_page: str | None = self._get_previous_page()

        return PaginatedObject(**{
            "data": data,
            'count': self.count,
            'total_pages': total_pages,
            'next_page': next_page,
            'previous_page': previous_page
        })


class StateStorage(Generic[T]):

    test_list = [
        Test(name='Pepi', test=77),
        Test(name='SuperTest', test=99)
    ]

    products_list = [
        Product(id='1', type=ProductType.BASIC),
        Product(id='2', type=ProductType.PLUS)
    ]

    customers_list: List[Customer] = mock_customers_list

    def __init__(self, dbConfig: DbConfig) -> None:
        pass

    # TODO: test it
    def _paginate(self, dataset_list: List[T], page: int, per_page: int):
        paginator = Paginator[T](dataset_list, page, per_page)
        return paginator.get_pagination()

    # TODO: consider create a class
    # TODO: type it
    # TODO: test it
    def _get_new_id(self, items, key) -> str:
        new_id = str(uuid.uuid4())
        all_ids = list(map(lambda elem: getattr(elem, key), items))

        if new_id not in all_ids:
            return new_id

        else:
            return self._get_new_id(items, key)

    # TODO: consider create a class
    # TODO: type it
    # TODO: test it
    def _validate_personal_id(self, id: str, exception: List[str] = []):
        all_ids = list(
            map(lambda customer: customer.personal_id if customer.personal_id not in exception else '', self.customers_list))

        if id in all_ids:
            return False

        return True

    # TODO: to be removed
    def test_database(self) -> List[Test]:
        return self.test_list

    def get_products_list(self) -> ProductList:
        products = self.products_list
        return ProductList(data=products)

    def get_product(self, id) -> Product:
        product = next((x for x in self.products_list if x.id == id), None)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id: {id} was not found")

        return product

    def get_customers_list(self, per_page: int, page: int) -> CustomerList:

        dataset: List[Customer] = self.customers_list
        response = self._paginate(dataset, page, per_page)

        parsed_response = CustomerList(**response)

        return parsed_response

    def get_customer_by_id(self, id: int) -> Customer:
        customer = next((x for x in self.customers_list if x.id == id), None)

        if not customer:
            raise resourceNotFound

        return customer

    def create_customer(self, customer: CustomerIn) -> Customer:
        is_personal_id_valid = self._validate_personal_id(customer.personal_id)

        if not is_personal_id_valid:
            raise noUniqueElement

        new_id = self._get_new_id(self.customers_list, 'id')

        new_customer = Customer(**{'id': new_id, **customer.dict()})
        self.customers_list.append(new_customer)

        return new_customer

    def update_customer(self, id: str, customer: CustomerIn) -> Customer:
        customer_index = next((ind for ind, customer in enumerate(
            self.customers_list) if customer.id == id), None)

        if customer_index == None:
            raise resourceNotFound

        current_customer = self.customers_list[customer_index]

        if customer.personal_id:
            is_personal_id_valid = self._validate_personal_id(
                customer.personal_id, [current_customer.personal_id])

            if not is_personal_id_valid:
                raise noUniqueElement

        updated_customer = {
            **current_customer.dict(),
            **customer.dict()
        }

        validated_customer = Customer(**updated_customer)

        self.customers_list[customer_index] = validated_customer

        return self.customers_list[customer_index]

    def delete_customer(self, id: str) -> None:
        customer_index = next((ind for ind, customer in enumerate(
            self.customers_list) if customer.id == id), None)

        if customer_index == None:
            raise resourceNotFound

        del self.customers_list[customer_index]
