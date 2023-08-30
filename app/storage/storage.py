from enum import Enum, auto
from typing import Protocol
from pydantic import EmailStr
from starlette.requests import Request

from app.models.users import User

from ..config import DbConfig
from .mongo_storage import MongoStorage

# from .postgres_storage import PostgresStorage
from .state_storage import StateStorage

from ..models.general import Test
from ..models.products import Product, ProductListCollection
from ..models.customers import Customer, CustomerPagination


class DatabaseType(Enum):
    MONGO = auto()
    POSTGRESQL = auto()
    MEMORY = auto()


class Storage(Protocol):
    def __init__(self, dbConfig: DbConfig) -> None:
        ...

    def test_database(self) -> list[Test]:
        ...

    def get_products_list(self) -> ProductListCollection:
        ...

    def get_product_by_id(self, id: int) -> Product:
        ...

    def get_customers_list(self, per_page: int, page: int) -> CustomerPagination:
        ...

    def get_customer_by_id(self, id: int) -> Customer:
        ...

    def create_customer(self, customer: Customer) -> Customer:
        ...

    def update_customer(self, id: int, customer: Customer) -> Customer:
        ...

    def delete_customer(self, id: int) -> None:
        ...

    def get_user(self, id: int | None = None, mail: EmailStr | None = None) -> User:
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
        # if type == DatabaseType.POSTGRESQL:
        #     return PostgresStorage(dbConfig=dbConfig)

        return StateStorage(dbConfig=dbConfig)
