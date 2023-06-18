from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional

from ..models.customers import Customer, CustomerIn, CustomerType
from ..storage.storage import StorageAccess
from ..exceptions.general_exceptions import noUniqueElement, resourceNotFound

router = APIRouter(
    prefix="/customers",
    tags=['Customers']
)

# TODO: Add HATEOAS
# TODO: Add sort and implement other filters (just add pagination...)


@router.get("/", response_model=List[Customer])
def get_customers_list(client=Depends(StorageAccess.get_db),
                       limit: int = 10,
                       skip: int = 0,
                       search: Optional[str] = ''):

    return client.get_customers_list()


@router.get("/{id}", response_model=Customer)
def get_customer(id: str, client=Depends(StorageAccess.get_db)):
    try:
        customer = client.get_customer(id)
        return customer

    except resourceNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

# TODO: implement HATEOAS


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: CustomerIn, client=Depends(StorageAccess.get_db)):
    try:
        new_customer = client.create_customer(customer)

        return new_customer

    except noUniqueElement:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Could not create the new customer. The personal ID {customer.personal_id} is already used.")

# TODO: auth issue: diference between banker (can edit all) and user (can edit only part of himself)


@router.put("/{id}", response_model=Customer)
def update_post(id: str, customer: CustomerIn, client=Depends(StorageAccess.get_db)):
    try:
        updated_customer = client.update_customer(id, customer)

        return updated_customer

    except resourceNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    except noUniqueElement:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Could not create the new customer. The personal ID {customer.personal_id} is already used.")
