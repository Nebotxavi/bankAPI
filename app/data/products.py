import time

from app.models.products import ProductIn, ProductType


mock_products_list = [
    {'type': ProductType.BASIC},
    {'type': ProductType.PLUS}
]


def parse_products(products_list):
    parsed_products: list[ProductIn] = []
    for product in products_list:
        parsed_products.append(ProductIn.model_validate(product))
        time.sleep(0.01)

    return parsed_products


mock_parsed_products = parse_products(mock_products_list)
