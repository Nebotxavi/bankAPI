import time
import uuid
from typing import List

from ..models.customers import Customer, CustomerType, NewCustomer

mock_customers_list = [
    # NewCustomer(
    {
        # "id":'bf18ad6a-6526-4e7c-9628-df1a555f1e4f',
        "personal_id": "18438695C",
        "family_name": "Pep",
        "middle_name": None,
        "surname": "Botifarra",
        "additional_surname": "Garcia",
        "customer_type": CustomerType.ANALYST
    },
    # NewCustomer(
    {
        # "id":'c2faccf6-b3cd-46a5-aff8-6ee2009317b3',
        "personal_id": "38528899F",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38558899A",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38998899B",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528877C",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899D",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899E",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38521199F",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899G",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899H",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899I",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899J",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899K",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899L",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899M",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    # NewCustomer(
    {
        # "id":str(uuid.uuid4()),
        "personal_id": "38528899N",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    }
]


def parse_customers(customers_list):
    parsed_customers: List[NewCustomer] = []
    for customer in customers_list:
        parsed_customers.append(NewCustomer.parse_obj(customer))
        time.sleep(0.01)

    return parsed_customers


mock_parsed_customers = parse_customers(mock_customers_list)
