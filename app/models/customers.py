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
    customer_type: CustomerType


class Customer(CustomerBase):
    id: str


class NewCustomer(CustomerBase):
    id: str = Field(default_factory=IdGenerator.get_id)


class CustomerIn(CustomerBase):
    pass


class CustomerList(PaginatedResponse):
    data: List[Customer]
