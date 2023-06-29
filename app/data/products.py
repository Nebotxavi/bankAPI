import time
from typing import List

from app.models.products import NewProduct, ProductType


mock_products_list = [
    {'type': ProductType.BASIC},
    {'type': ProductType.PLUS}
]


def parse_products(products_list):
    parsed_products: List[NewProduct] = []
    for product in products_list:
        parsed_products.append(NewProduct.parse_obj(product))
        time.sleep(0.01)

    return parsed_products


mock_parsed_products = parse_products(mock_products_list)
