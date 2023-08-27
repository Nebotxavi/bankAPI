from app.models.products import Product, ProductType, ProductListCollection


def test_get_all_products(authorized_client):
    res = authorized_client.get('/products/')

    def validate(product):
        return Product.model_validate(product)

    content = res.json()

    ProductListCollection.model_validate(content)
    products_map = map(validate, content['data'])
    products = list(products_map)

    assert content.get('count', None) == None
    assert content.get('total_pages', None) == None
    assert len(products)
    assert res.status_code == 200


def test_get_product(authorized_client, products):
    res = authorized_client.get(f'/products/{products[0].id}')

    product = Product.model_validate(res.json())

    assert product.id == products[0].id
    assert type(product.type) == ProductType
    assert res.status_code == 200
