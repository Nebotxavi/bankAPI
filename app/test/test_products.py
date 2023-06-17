from app.models.products import Product, ProductType


def test_get_all_products(client):
    res = client.get('/products/')

    def validate(product):
        return Product(**product)

    products_map = map(validate, res.json())
    products = list(products_map)

    assert len(products)
    assert res.status_code == 200


def test_get_product(client, products):
    res = client.get(f'/products/{products[0].id}')

    product = Product(**res.json())

    assert product.id == products[0].id
    assert type(product.type) == ProductType
    assert res.status_code == 200
