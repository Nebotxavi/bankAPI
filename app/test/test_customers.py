from copy import copy

from fastapi import status
from fastapi.encoders import jsonable_encoder
from app.models.customers import Customer, CustomerBasic, CustomerType, CustomerIn, CustomerPagination


def test_get_customers(authorized_client, test_customers: list[Customer]):

    res = authorized_client.get('/customers/')

    def validate(customer):
        return CustomerBasic.model_validate(customer.model_dump())

    response = CustomerPagination.model_validate(res.json())

    customers_map = map(validate, response.data)
    customers = list(customers_map)
    count = response.count
    total_pages = response.total_pages

    assert count == len(test_customers)
    assert total_pages == len(test_customers) // len(customers) + 1 if len(
        test_customers) % len(customers) else len(test_customers) // len(customers)
    assert len(customers) > 0
    assert res.status_code == 200


def test_get_customers_with_pagination_params(authorized_client, test_customers: list[Customer]):
    per_page = 5
    page = 2

    res = authorized_client.get(f'/customers/?per_page={per_page}&page={page}')

    def validate(customer):
        return CustomerBasic.model_validate(customer.model_dump())

    response = CustomerPagination.model_validate(res.json())

    customers_map = map(validate, response.data)
    customers = list(customers_map)
    count = response.count
    total_pages = response.total_pages

    assert len(customers) >= 5
    for ind, customer in enumerate(customers):
        test_customer = CustomerBasic(**test_customers[ind + per_page].model_dump())
        assert customer.id == test_customer.id
        assert customer.personal_id == test_customer.personal_id
        assert customer.href
        if (customer.href):
            assert str(customer.id) in customer.href

    assert count == len(test_customers)
    if count:
        assert total_pages == count // per_page + \
            1 if count % per_page else count // per_page
    assert res.status_code == status.HTTP_200_OK


def test_get_customers_with_wrong_page(authorized_client):
    page = 8888888
    res = authorized_client.get(f'/customers/?page={page}')

    content = res.json()

    assert res.status_code == status.HTTP_200_OK
    assert len(content['data']) == 0


def test_get_customers_with_wrong_pagination_params(authorized_client):
    res = authorized_client.get(f'/customers/?per_page=7&page=2')

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_customer(authorized_client, test_customers: list[Customer]):
    res = authorized_client.get(f'/customers/{test_customers[0].id}')
    customer = Customer.model_validate(res.json())

    assert res.status_code == status.HTTP_200_OK
    assert customer.id == test_customers[0].id
    assert customer.personal_id == test_customers[0].personal_id
    assert customer.family_name == test_customers[0].family_name
    assert customer.middle_name == test_customers[0].middle_name
    assert customer.surname == test_customers[0].surname
    assert customer.additional_surname == test_customers[0].additional_surname
    assert customer.customer_type == test_customers[0].customer_type


def test_get_customer_not_exist(authorized_client):
    res = authorized_client.get('/customers/88888888')

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_customer(authorized_client):
    new_customer = {
        "personal_id": "2233869KC",
        "family_name": "Antionet",
        "surname": "Hazel",
        "additional_surname": "Vilar",
        "customer_type": "Analyst"
    }

    res = authorized_client.post('/customers/', json=jsonable_encoder(new_customer))

    received_customer = Customer.model_validate(res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert received_customer.personal_id == new_customer['personal_id']
    assert received_customer.family_name == new_customer['family_name']
    assert received_customer.additional_surname == new_customer['additional_surname']
    assert received_customer.customer_type == CustomerType(
        new_customer['customer_type'])


def test_new_customer_ID_is_higher_than_previous(authorized_client, test_customers: list[Customer]):
    new_customer = {
        "personal_id": "2233869KD",
        "family_name": "Antionet",
        "surname": "Hazel",
        "additional_surname": "Vilar",
        "customer_type": "Analyst"
    }

    res = authorized_client.post('/customers/', json=jsonable_encoder(new_customer))

    received_customer = Customer.model_validate(res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert int(received_customer.id) > int(test_customers[-2].id)


def test_create_wrong_customer(authorized_client):
    new_customer = {
        "personal_id": "18438695C",
        "family_name": "Antionet",
        "surname": "Hazel",
    }

    res = authorized_client.post('/customers/', json=jsonable_encoder(new_customer))

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_customer_with_personal_id_already_used(authorized_client, test_customers: list[Customer]):
    new_customer = {
        "personal_id": test_customers[0].personal_id,
        "family_name": "Antionet",
        "surname": "Hazel",
        "additional_surname": "Vilar",
        "customer_type": "Analyst"
    }

    res = authorized_client.post('/customers/', json=jsonable_encoder(new_customer))

    assert res.status_code == status.HTTP_409_CONFLICT


def test_update_customer(authorized_client, test_customers: list[Customer]):
    customer = copy(test_customers[0])
    customer.family_name = "Walden"

    res = authorized_client.put(
        f'/customers/{customer.id}', json=jsonable_encoder(customer))
    received_customer = Customer.model_validate(res.json())

    assert res.status_code == status.HTTP_200_OK
    assert received_customer.family_name == customer.family_name


def test_updated_with_wrong_id(authorized_client, test_customers: list[Customer]):
    customer = copy(test_customers[0])
    customer.family_name = "Walden"

    res = authorized_client.put(
        f'/customers/8888888', json=jsonable_encoder(customer))

    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_with_wrong_data(authorized_client, test_customers: list[Customer]):
    current_customer = test_customers[0]

    updated_customer = {
        "personal_id": current_customer.personal_id,
        "middle_name": current_customer.middle_name,
        "additional_surname": current_customer.additional_surname,
        "customer_type": current_customer.customer_type.value
    }

    res = authorized_client.put(
        f'/customers/{test_customers[0].id}', json=jsonable_encoder(updated_customer))

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_with_used_personal_id(authorized_client, test_customers: list[Customer]):
    customer = copy(test_customers[0])
    other_customer = test_customers[1]

    customer.personal_id = other_customer.personal_id

    res = authorized_client.put(
        f'/customers/{test_customers[0].id}', json=jsonable_encoder(customer))

    assert res.status_code == status.HTTP_409_CONFLICT


def test_update_with_blank_optional_data(authorized_client, test_customers: list[Customer]):
    current_customer = copy(test_customers[0])

    updated_customer = {
        "id": current_customer.id,
        "personal_id": current_customer.personal_id,
        "family_name": 'Walden',
        "surname": current_customer.surname,
        "customer_type": current_customer.customer_type.value
    }

    res = authorized_client.put(
        f'/customers/{test_customers[0].id}', json=jsonable_encoder(updated_customer))
    received_customer = Customer.model_validate(res.json())

    assert res.status_code == status.HTTP_200_OK
    assert received_customer.middle_name == None
    assert received_customer.additional_surname == None


def test_delete_customer(authorized_client, test_customers: list[Customer]):
    res = authorized_client.delete(f'/customers/{test_customers[0].id}')

    assert res.status_code == status.HTTP_200_OK


def test_delete_wrong_customer(authorized_client, test_customers: list[Customer]):
    res = authorized_client.delete('customers/888888888')

    assert res.status_code == status.HTTP_404_NOT_FOUND
