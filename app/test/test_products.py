from app.models.products import Product, ProductType    
from app.models.customers import Customer

def test_get_all_products(client):
    res = client.get('/products/')

    def validate(product):
        return Product(**product)

    posts_map = map(validate, res.json())
    posts = list(posts_map)

    assert len(posts)
    assert res.status_code == 200

def test_get_product(client):
    res = client.get('/products/1')

    product = Product(**res.json())

    assert product.id == 1
    assert type(product.type) == ProductType

#  --------------- REMOVE ----------------------

def test_get_customer(client, test_customers):

    assert len(test_customers) == 3
    assert type(test_customers[0]) == Customer
    assert test_customers[0].family_name == 'Alphonese'