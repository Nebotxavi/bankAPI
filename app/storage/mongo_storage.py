from pymongo.mongo_client import MongoClient
from typing import List

from ..config import DbConfig
from ..models.test import DatabaseTest


class MongoStorage:
    def __init__(self, dbConfig: DbConfig) -> None:
        self.client = MongoClient(f"mongodb+srv://{dbConfig.mongo_username}:{dbConfig.mongo_password}@cluster0.6ijuskv.mongodb.net/?retryWrites=true&w=majority")

    # TODO: find the way to avoid writing the database and collection with strings
    def test_database(self) -> List[DatabaseTest]:
        return list(self.client.bankAPI.health.find({},{'_id': 0}))