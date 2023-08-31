from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Literal
from typing_extensions import Annotated
from app.auth.oauth2 import get_current_user

from app.http.hateoas import HateoasManager

from ..models.customers import Customer, CustomerBasic, CustomerIn, CustomerPagination
from ..storage.storage import Storage, StorageAccess
from ..exceptions.general_exceptions import (
    ImmutableFieldError,
    NoUniqueElement,
    ResourceNotFound,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=CustomerPagination)
def get_customers_list(
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
    per_page: Literal["5", "10", "25"] = "10",
    page: Annotated[int, Query(gt=0)] = 1,
    sort_by: str | None = None,
    direction: Literal['-1', '1'] = '1',
    search: str = ''
):
    # TODO: SORT

    # TODO: SEARCH
    customers: CustomerPagination = client.get_customers_list(int(per_page), page, sort_by, int(direction), search)

    hateoas = HateoasManager[CustomerBasic](customers.data, "customers", key="id")
    hateoas.set_urls()

    return customers


@router.get("/{id}", response_model=Customer)
def get_customer(
    id: int,
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        customer: Customer = client.get_customer_by_id(id)
        return customer

    except ResourceNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found",
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(
    customer: CustomerIn,
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        parsed_customer = Customer.model_validate(customer.model_dump())
        new_customer: Customer = client.create_customer(parsed_customer)

        return new_customer

    except NoUniqueElement:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Could not create the new customer. The personal ID {customer.personal_id} is already used.",
        )


@router.put("/{id}", response_model=Customer)
def update_customer(
    id: int,
    customer: Customer,
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        updated_customer: Customer = client.update_customer(id, customer)

        return updated_customer

    except ResourceNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found",
        )
    except NoUniqueElement:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Could not update the customer. The personal ID {customer.personal_id} is already used.",
        )

    except ImmutableFieldError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.delete("/{id}")
def delete_customer(
    id: int,
    client: Storage = Depends(StorageAccess.get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        client.delete_customer(id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"User with id: {id} has been removed."},
        )

    except ResourceNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found.",
        )
