from fastapi import HTTPException, status
from typing import List

from ..config import DbConfig
from ..models.products import ProductType, Product
from ..models.customers import CustomerType, Customer, CustomerIn
from ..models.general import Test

class StateStorage:

    test_list = [
        Test(name= 'Pepi', test= 77),
        Test(name= 'SuperTest', test= 99)
        ]

    products_list = [
        Product(id= 1, type= ProductType.BASIC),
        Product(id= 2, type= ProductType.PLUS)
        ]

    customers_list: List[Customer] = [
        Customer(
            id=1,
            personal_id= "18438695C",
            family_name= "Pep",
            middle_name= None,
            surname= "Botifarra",
            additional_surname= "Garcia",
            customer_type= CustomerType.ANALYST
        ),
        Customer(
            id=2,
            personal_id= "38528899F",
            family_name= "Ruben",
            middle_name= "Von",
            surname= "Rnauf",
            additional_surname= None,
            customer_type= CustomerType.STANDARD
            )   
    ]

    def __init__(self, dbConfig: DbConfig) -> None:
        pass

    def _get_new_id(self, items, key) -> int:
        latest_id = list(map(lambda product: getattr(product, key), items))

        return max(latest_id) + 1 if latest_id else 0

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"User with id: {id} was not found")

        return customer

    def create_customer(self, customer: CustomerIn) -> Customer:
        new_id = self._get_new_id(self.customers_list, 'id')

        new_customer = Customer(**{'id': new_id, **customer.dict()})
        self.customers_list.append(new_customer)

        return new_customer