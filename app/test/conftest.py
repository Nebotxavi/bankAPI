from fastapi import Depends
from fastapi.testclient import TestClient
import pytest

from app.storage.storage import StorageFactory, DatabaseType, StorageAccess
from app.models.customers import CustomerType, CustomerIn
from app.config import dbConfig
from app.main import app

app.state.db = StorageFactory.get_storage(DatabaseType.STATE, dbConfig)


@pytest.fixture
def client():
    client = TestClient(app)

    return client


@pytest.fixture
def products():
    client_state = app.state.db
    return client_state.products_list


@pytest.fixture
def test_customers():
    client_state = app.state.db
    test_customers_list = [
        {
            "personal_id": '62819372V',
            "family_name": "Alphonse",
            "middle_name": None,
            "surname": 'Mucha',
            "additional_surname": None,
            "customer_type": CustomerType.STANDARD
        },
        {
            "personal_id": '33942831U',
            "family_name": "Xiaoxiang",
            "surname": 'Cheng',
            "customer_type": CustomerType.STANDARD
        },
        {
            "personal_id": '83335212G',
            "family_name": "Paco",
            "middle_name": 'Lars',
            "surname": 'Gimenez',
            "additional_surname": "Gonzalo",
            "customer_type": CustomerType.ANALYST
        }
    ]

    customers = client_state.customers_list

    for test_customer in test_customers_list:
        customer = CustomerIn(**test_customer)

        new_customer = client_state.create_customer(customer)
        customers.append(new_customer)

    return customers
