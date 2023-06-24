from pymongo.mongo_client import MongoClient
from typing import List, Dict, Union

from ..config import DbConfig
from ..models.general import Test
from ..models.products import Product, ProductList
from ..models.customers import Customer, CustomerIn, CustomerList


class MongoStorage:
    def __init__(self, dbConfig: DbConfig) -> None:
        self.client = MongoClient(f"mongodb+srv://{dbConfig.mongo_username}:{dbConfig.mongo_password}@cluster0.6ijuskv.mongodb.net/?retryWrites=true&w=majority")
        self.database = dbConfig.db_name

    def test_database(self) -> List[Test]:
        return list(self.client[self.database].health.find({},{'_id': 0}))

    def get_products_list(self) -> ProductList:
        ...

    def get_product(self, id) -> Product:
        ...

    def get_customers_list(self, amount: int, page:int) -> CustomerList:
        ...

    def get_customer_by_id(self, id: int) -> Customer:
        ...

    def create_customer(self, customer: CustomerIn) -> Customer:
        ...

    def update_customer(self, id, customer: CustomerIn) -> Customer:
        ...