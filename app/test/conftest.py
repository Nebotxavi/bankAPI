from fastapi.testclient import TestClient
import pytest
from app.auth.oauth2 import create_access_token
from app.models.users import User


from app.storage.storage import Storage, StorageFactory, DatabaseType
from app.models.customers import CustomerType, CustomerIn, Customer
from app.models.products import Product
from app.data.users import mock_users_list
from app.config import dbConfig
from app.main import app

app.state.db = StorageFactory.get_storage(DatabaseType.MEMORY, dbConfig)


@app.on_event("startup")
def create_test_customers() -> list[Customer]:
    storage: Storage = app.state.db
    customers = []

    test_customers_list = [
        {
            "personal_id": "62819372V",
            "family_name": "Alphonse",
            "middle_name": None,
            "surname": "Mucha",
            "additional_surname": None,
            "customer_type": CustomerType.STANDARD,
        },
        {
            "personal_id": "33942831U",
            "family_name": "Xiaoxiang",
            "surname": "Cheng",
            "customer_type": CustomerType.STANDARD,
        },
        {
            "personal_id": "83335212G",
            "family_name": "Paco",
            "middle_name": "Lars",
            "surname": "Gimenez",
            "additional_surname": "Gonzalo",
            "customer_type": CustomerType.ANALYST,
        },
    ]

    for test_customer in test_customers_list:
        customer = CustomerIn.model_validate(test_customer)

        new_customer = storage.create_customer(Customer.model_validate(customer.model_dump()))
        customers.append(new_customer)

    return customers


@pytest.fixture
def storage():
    return app.state.db


@pytest.fixture
def client():
    client = TestClient(app)

    return client


@pytest.fixture
def test_user() -> User:
    storage = app.state.db
    return storage.get_user(mail=mock_users_list[0]["mail"])


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user.id})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def products() -> list[Product]:
    storage = app.state.db

    return storage.products_list


@pytest.fixture
def test_customers() -> list[Customer]:
    storage = app.state.db

    return storage.customers_list
