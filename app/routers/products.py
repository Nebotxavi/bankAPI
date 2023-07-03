from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.exceptions.general_exceptions import resourceNotFound

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
    try:
        product = client.get_product_by_id(id)

        return product
    except resourceNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id: {id} was not found")
