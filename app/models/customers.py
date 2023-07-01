from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

from app.utils.utils import IdGenerator

from .general import PaginatedResponse


class CustomerType(Enum):
    STANDARD = "Standard"
    ANALYST = "Analyst"


class CustomerBase(BaseModel):
    personal_id: str
    family_name: str
    middle_name: Optional[str] = None
    surname: str
    additional_surname: Optional[str] = None
    # customer_type: CustomerType


class CustomerDetail(CustomerBase):
    customer_type: CustomerType


class Customer(CustomerDetail):
    id: int


class CustomerIn(CustomerDetail):
    pass


class NewCustomer(CustomerIn):
    id: int = Field(default_factory=IdGenerator.get_id)


class CustomerBasic(CustomerBase):
    id: int
    href: Optional[str] = None


class CustomerPagination(PaginatedResponse):
    data: List[CustomerBasic]
