from app.models.products import Product, ProductType, ProductListCollection


def test_get_all_products(client):
    res = client.get('/products/')

    def validate(product):
        return Product.parse_obj(product)

    content = res.json()

    ProductListCollection.parse_obj(content)
    products_map = map(validate, content['data'])
    products = list(products_map)

    assert content.get('count', None) == None
    assert content.get('total_pages', None) == None
    assert len(products)
    assert res.status_code == 200


def test_get_product(client, products):
    res = client.get(f'/products/{products[0].id}')

    product = Product.parse_obj(res.json())

    assert product.id == products[0].id
    assert type(product.type) == ProductType
    assert res.status_code == 200
