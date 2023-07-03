from pydantic import EmailStr
from pymongo.mongo_client import MongoClient
from typing import List, Dict

from app.models.users import User

from ..config import DbConfig
from ..models.general import Test
from ..models.products import Product, ProductListCollection
from ..models.customers import Customer, CustomerIn, CustomerPagination


class MongoStorage:
    def __init__(self, dbConfig: DbConfig) -> None:
        self.client = MongoClient(
            f"mongodb+srv://{dbConfig.mongo_username}:{dbConfig.mongo_password}@cluster0.6ijuskv.mongodb.net/?retryWrites=true&w=majority")
        self.database = dbConfig.db_name

    def test_database(self) -> List[Test]:
        return list(self.client[self.database].health.find({}, {'_id': 0}))

    def get_products_list(self) -> ProductListCollection:
        ...

    def get_product_by_id(self, id) -> Product:
        ...

    def get_customers_list(self, per_page: int, page: int) -> CustomerPagination:
        ...

    def get_customer_by_id(self, id: int) -> Customer:
        ...

    def create_customer(self, customer: CustomerIn) -> Customer:
        ...

    def update_customer(self, id, customer: CustomerIn) -> Customer:
        ...

    def delete_customer(self, id: str) -> None:
        ...

    def get_user(self, id: int | None, mail: EmailStr | None) -> User:
        ...
