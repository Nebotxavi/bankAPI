from fastapi import HTTPException, status
from typing import List
import uuid

from ..config import DbConfig
from ..models.products import ProductType, Product
from ..models.customers import CustomerType, Customer, CustomerIn
from ..models.general import Test
from ..exceptions.general_exceptions import noUniqueElement, resourceNotFound


class StateStorage:

    test_list = [
        Test(name='Pepi', test=77),
        Test(name='SuperTest', test=99)
    ]

    products_list = [
        Product(id='1', type=ProductType.BASIC),
        Product(id='2', type=ProductType.PLUS)
    ]

    customers_list: List[Customer] = [
        Customer(
            id='bf18ad6a-6526-4e7c-9628-df1a555f1e4f',
            personal_id="18438695C",
            family_name="Pep",
            middle_name=None,
            surname="Botifarra",
            additional_surname="Garcia",
            customer_type=CustomerType.ANALYST
        ),
        Customer(
            id='c2faccf6-b3cd-46a5-aff8-6ee2009317b3',
            personal_id="38528899F",
            family_name="Ruben",
            middle_name="Von",
            surname="Rnauf",
            additional_surname=None,
            customer_type=CustomerType.STANDARD
        )
    ]

    def __init__(self, dbConfig: DbConfig) -> None:
        pass

    def _get_new_id(self, items, key) -> str:
        new_id = str(uuid.uuid4())
        all_ids = list(map(lambda elem: getattr(elem, key), items))

        if new_id not in all_ids:
            return new_id

        else:
            return self._get_new_id(self, items, key)

    def _validate_personal_id(self, id: str, exception: List[str] = []):
        all_ids = list(
            map(lambda customer: customer.personal_id if customer.personal_id not in exception else '', self.customers_list))

        if id in all_ids:
            return False

        return True

    # TODO: to be removed
    def test_database(self) -> List[Test]:
        return self.test_list

    def get_products_list(self) -> List[Product]:
        return self.products_list

    def get_product(self, id) -> Product:
        product = next((x for x in self.products_list if x.id == id), None)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product with id: {id} was not found")

        return product

    # TODO: implement pagination
    def get_customers_list(self) -> List[Customer]:
        return self.customers_list

    def get_customer(self, id: int) -> Customer:
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

        updated_customer = {
            **self.customers_list[customer_index].dict(),
            **customer.dict()
        }

        if customer.personal_id:

            is_personal_id_valid = self._validate_personal_id(
                customer.personal_id, [updated_customer['personal_id']])

            if not is_personal_id_valid:
                raise noUniqueElement

        validated_customer = Customer(**updated_customer)

        self.customers_list[customer_index] = validated_customer

        return self.customers_list[customer_index]
