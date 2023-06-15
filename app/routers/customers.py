from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional

from ..models.customers import Customer, CustomerIn, CustomerType
from ..storage.storage import StorageAccess

router = APIRouter(
    prefix="/customers",
    tags=['Customers']
)

# TODO: Add HATEOAS
# TODO: Add sort and implement other filters (just add pagination...)
@router.get("/", response_model=List[Customer])
def get_customers_list(client = Depends(StorageAccess.get_db), 
                       limit: int = 10, 
                       skip: int = 0, 
                       search: Optional[str] = ''):

    return client.get_customers_list()

@router.get("/{id}", response_model=Customer)
def get_customer(id: str, client = Depends(StorageAccess.get_db)):
    customer = client.get_customer(id)
    return customer 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer: CustomerIn, client = Depends(StorageAccess.get_db)):
    new_customer = client.create_customer(customer)

    return new_customer

# TODO: auth issue: diference between banker (can edit all) and user (can edit only part of himself)
@router.put("/", response_model=Customer)
def update_post(id: str, customer: Customer):
    pass