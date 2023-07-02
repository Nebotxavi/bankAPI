import pytest
from fastapi import status, Request
from typing import List

from app.http.hateoas import HateoasManager, HrefProvider
from app.middleware.middleware import request_object
from app.models.customers import CustomerBasic

BASE_URL = 'http://localhost:8000'
TESTING_PATH = "/this_is_a_testing_path/"


@pytest.fixture(autouse=True)
def provide_request():
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": TESTING_PATH,
        "query_string": b"",
        "headers": [],
        "server": ('localhost', 8000)
    }

    request = Request(scope=scope)
    token = request_object.set(request)
    yield

    request_object.reset(token)


def test_href_provider_get_url_with_params():

    url = HrefProvider.get_url_with_params({'param1': 1, 'param2': 'value2'})

    assert '1' in str(url)
    assert 'value2' in str(url)
    assert str(url) == f'{BASE_URL}{TESTING_PATH}?param1=1&param2=value2'


def test_href_get_url_with_params_without_params():
    url = HrefProvider.get_url_with_params()
    assert str(url) == BASE_URL + TESTING_PATH


def test_hateoas_manager_set_urls_with_id(test_customers):
    customers: List[CustomerBasic] = [CustomerBasic.parse_obj(
        customer) for customer in test_customers]

    hateoas = HateoasManager[CustomerBasic](
        customers, 'customers', key='id')
    hateoas.set_urls()

    for customer in customers:
        assert customer.href

        if customer.href:
            assert str(customer.id) in customer.href
            assert customer.href == f'{BASE_URL}/customers/{customer.id}'


def test_hateoas_manager_set_url_with_key(test_customers):
    customer: CustomerBasic = CustomerBasic.parse_obj(test_customers[0])

    hateoas = HateoasManager[CustomerBasic](
        [customer], 'customers', ref=f"test_resource_path_{customer.id}")
    hateoas.set_urls()

    assert customer.href

    if customer.href:
        assert str(customer.id) in customer.href
        assert "test_resource_path" in customer.href
        assert customer.href == f'{BASE_URL}/customers/test_resource_path_{customer.id}'


def test_hateoas_manager_set_url_without_id_or_key(test_customers):
    customers: List[CustomerBasic] = [CustomerBasic.parse_obj(
        customer) for customer in test_customers]

    hateoas = HateoasManager[CustomerBasic](
        customers, 'customers')
    hateoas.set_urls()

    for customer in customers:
        assert customer.href

        if customer.href:
            assert customer.href == f'{BASE_URL}/customers/'
