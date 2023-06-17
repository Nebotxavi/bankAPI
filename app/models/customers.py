from pydantic import BaseModel
from typing import Optional
from enum import Enum


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


class CustomerIn(CustomerBase):
    pass
