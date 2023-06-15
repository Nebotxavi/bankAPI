from app.models.products import Product, ProductType

def test_user_get_all_products(client):
    res = client.get('/products/')

    def validate(product):
        return Product(**product)

    posts_map = map(validate, res.json())
    posts = list(posts_map)

    # TODO: to be removed
    assert getattr(posts[0], 'type') == ProductType.PLUS
    assert res.status_code == 200