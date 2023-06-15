from fastapi.testclient import TestClient
import pytest

from app.storage.storage import StorageFactory, DatabaseType
from app.config import dbConfig
from app.main import app

app.state.db = StorageFactory.get_storage(DatabaseType.STATE, dbConfig)

@pytest.fixture
def client():
    client = TestClient(app)

    return client