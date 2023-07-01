from fastapi import APIRouter, Depends
from typing import List

from ..models.products import Product, ProductListCollection
from ..storage.storage import StorageAccess

router = APIRouter(
    prefix="/products",
    tags=['Products']
)


@router.get('/', response_model=ProductListCollection)
def get_products_list(client=Depends(StorageAccess.get_db)):

    products_list = client.get_products_list()

    return products_list


@router.get('/{id}/', response_model=Product)
def get_product(id: int, client=Depends(StorageAccess.get_db)):
    product = client.get_product_by_id(id)

    return product
