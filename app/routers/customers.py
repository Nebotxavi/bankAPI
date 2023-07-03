from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Path
from typing import List, Optional, Literal
from typing_extensions import Annotated
from pydantic import Field
from app.auth.oauth2 import get_current_user

from app.http.hateoas import HateoasManager, HrefProvider

from ..models.customers import Customer, CustomerBasic, CustomerIn, CustomerType, CustomerPagination
from ..storage.storage import StorageAccess
from ..exceptions.general_exceptions import noUniqueElement, resourceNotFound

router = APIRouter(
    prefix="/customers",
    tags=['Customers']
)


@router.get("/", response_model=CustomerPagination)
def get_customers_list(
    client=Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
    per_page: Literal['5', '10', '25'] = '10',
    page: Annotated[int, Query(gt=0)] = 1
):
    # TODO: SORT

    # TODO: SEARCH

    customers: CustomerPagination = client.get_customers_list(
        int(per_page), page)

    hateoas = HateoasManager[CustomerBasic](
        customers.data, 'customers', key='id')
    hateoas.set_urls()

    return customers


@router.get("/{id}", response_model=Customer)
def get_customer(id: int, client=Depends(StorageAccess.get_db), current_user: int = Depends(get_current_user),):
    try:
        customer: Customer = client.get_customer_by_id(id)
        return customer

    except resourceNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: CustomerIn, client=Depends(StorageAccess.get_db), current_user: int = Depends(get_current_user)):
    try:
        new_customer: Customer = client.create_customer(customer)

        return new_customer

    except noUniqueElement:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Could not create the new customer. The personal ID {customer.personal_id} is already used.")


@router.put("/{id}", response_model=Customer)
def update_customer(
        id: int,
        customer: CustomerIn, client=Depends(StorageAccess.get_db),
        current_user: int = Depends(get_current_user),):
    try:
        updated_customer: Customer = client.update_customer(id, customer)

        return updated_customer

    except resourceNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    except noUniqueElement:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Could not update the customer. The personal ID {customer.personal_id} is already used.")


@router.delete("/{id}", response_model=Customer)
def delete_customer(id: int, client=Depends(StorageAccess.get_db), current_user: int = Depends(get_current_user),):
    try:
        client.delete_customer(id)

        return Response(status_code=status.HTTP_204_NO_CONTENT,
                        content=f'User with id: {id} has been removed.')

    except resourceNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found.")
