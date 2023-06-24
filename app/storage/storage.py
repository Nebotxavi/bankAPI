from enum import Enum, auto
from typing import Protocol, List
from starlette.requests import Request

from ..config import DbConfig
from .mongo_storage import MongoStorage
from .postgres_storage import PostgresStorage
from .state_storage import StateStorage

from ..models.general import Test
from ..models.products import Product, ProductList
from ..models.customers import Customer, CustomerIn, CustomerList


class DatabaseType(Enum):
    MONGO = auto()
    POSTGRESQL = auto()
    STATE = auto()


class Storage(Protocol):
    def __init__(self, dbConfig: DbConfig) -> None:
        ...

    def test_database(self) -> List[Test]:
        ...

    def get_products_list(self) -> ProductList:
        ...

    def get_product(self, id) -> Product:
        ...

    def get_customers_list(self, per_page: int, page:int) -> CustomerList:
        ...

    def get_customer_by_id(self, id) -> Customer:
        ...

    def create_customer(self, customer: CustomerIn) -> Customer:
        ...

    def update_customer(self, id, customer) -> Customer:
        ...


class StorageAccess:
    @staticmethod
    def get_db(request: Request) -> Storage:
        return request.app.state.db


class StorageFactory:
    @staticmethod
    def get_storage(type: DatabaseType, dbConfig: DbConfig) -> Storage:
        if type == DatabaseType.MONGO:
            return MongoStorage(dbConfig=dbConfig)
        if type == DatabaseType.POSTGRESQL:
            return PostgresStorage(dbConfig=dbConfig)

        return StateStorage(dbConfig=dbConfig)
