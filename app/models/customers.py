from pydantic import BaseModel, Field
from typing import List
from enum import Enum

from app.utils.utils import IdGenerator

from .general import PaginatedResponse


class CustomerType(Enum):
    STANDARD = "Standard"
    ANALYST = "Analyst"


class CustomerBase(BaseModel):
    personal_id: str
    family_name: str
    middle_name: str | None = None
    surname: str
    additional_surname: str | None = None


class CustomerDetail(CustomerBase):
    customer_type: CustomerType


class Customer(CustomerDetail):
    id: int = Field(default_factory=IdGenerator.get_id)


class CustomerIn(CustomerDetail):
    pass


class CustomerBasic(CustomerBase):
    id: int
    href: str | None = None


class CustomerPagination(PaginatedResponse):
    data: List[CustomerBasic]
