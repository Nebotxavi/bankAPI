import time
import uuid
from typing import List

from ..models.customers import CustomerType, Customer

mock_customers_list = [
    {
        "personal_id": "18438695C",
        "family_name": "Pep",
        "middle_name": None,
        "surname": "Botifarra",
        "additional_surname": "Garcia",
        "customer_type": CustomerType.ANALYST
    },
    {
        "personal_id": "38528899F",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38558899A",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38998899B",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528877C",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899D",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899E",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38521199F",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899G",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899H",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899I",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899J",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899K",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899L",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899M",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    },
    {
        "personal_id": "38528899N",
        "family_name": "Ruben",
        "middle_name": "Von",
        "surname": "Rnauf",
        "additional_surname": None,
        "customer_type": CustomerType.STANDARD
    }
]


def parse_customers(customers_list):
    parsed_customers: List[Customer] = []
    for customer in customers_list:
        parsed_customers.append(Customer.parse_obj(customer))
        time.sleep(0.01)

    return parsed_customers


mock_parsed_customers = parse_customers(mock_customers_list)
