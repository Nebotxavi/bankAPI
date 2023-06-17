from fastapi import status
from app.models.customers import Customer, CustomerType


def test_get_customers(client, test_customers):

    res = client.get(f'/customers/')

    def validate(customer):
        return Customer(**customer)

    customers_map = map(validate, res.json())
    customers = list(customers_map)

    assert len(customers) == len(test_customers)
    assert res.status_code == 200


def test_get_customer(client, test_customers):
    res = client.get(f'/customers/{test_customers[0].id}')

    customer = Customer(**res.json())

    assert res.status_code == status.HTTP_200_OK
    assert customer.id == test_customers[0].id
    assert customer.personal_id == test_customers[0].personal_id
    assert customer.family_name == test_customers[0].family_name
    assert customer.middle_name == test_customers[0].middle_name
    assert customer.surname == test_customers[0].surname
    assert customer.additional_surname == test_customers[0].additional_surname
    assert customer.customer_type == test_customers[0].customer_type


def test_get_customer_not_exist(client):
    res = client.get('/customers/88888888')

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_customer(client):
    new_customer = {
        "personal_id": "18438695C",
        "family_name": "Antionet",
        "surname": "Hazel",
        "additional_surname": "Vilar",
        "customer_type": "Analyst"
    }

    res = client.post('/customers/', json=new_customer)

    received_customer = Customer(**res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert received_customer.personal_id == new_customer['personal_id']
    assert received_customer.family_name == new_customer['family_name']
    assert received_customer.additional_surname == new_customer['additional_surname']
    assert received_customer.customer_type == CustomerType(
        new_customer['customer_type'])


def test_create_wrong_customer(client):
    new_customer = {
        "personal_id": "18438695C",
        "family_name": "Antionet",
        "surname": "Hazel",
    }

    res = client.post('/customers/', json=new_customer)

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
