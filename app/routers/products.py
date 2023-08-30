from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.oauth2 import get_current_user

from app.exceptions.general_exceptions import ResourceNotFound

from ..models.products import Product, ProductListCollection
from ..storage.storage import Storage, StorageAccess

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=ProductListCollection)
def get_products_list(
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
):
    products_list = client.get_products_list()

    return products_list


@router.get("/{id}/", response_model=Product)
def get_product(
    id: int,
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        product = client.get_product_by_id(id)

        return product
    except ResourceNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {id} was not found",
        )
