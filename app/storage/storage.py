from enum import Enum, auto
from typing import Protocol, List
from starlette.requests import Request

from ..config import DbConfig
from .mongo_storage import MongoStorage
from .postgres_storage import PostgresStorage


from ..models.test import DatabaseTest

class DatabaseType(Enum):
    MONGO = auto()
    POSTGRESQL = auto()

class Storage(Protocol):
    def __init__(self, dbConfig: DbConfig) -> None:
        ...
    
    def test_database(self) -> List[DatabaseTest]:
        ...

class StorageAccess:
    @staticmethod
    def get_db(request: Request): # TODO: type the output
        return request.app.state.db

class StorageFactory:
    @staticmethod
    def get_storage(type: DatabaseType, dbConfig: DbConfig) -> Storage:
        if type == DatabaseType.MONGO:
            return MongoStorage(dbConfig=dbConfig)
        if type == DatabaseType.POSTGRESQL:
            return PostgresStorage(dbConfig=dbConfig)
        else:
            raise Exception('Wrong database configuration')

    