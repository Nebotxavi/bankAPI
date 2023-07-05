from fastapi import Query
from pydantic import BaseModel, Field
from typing import Annotated, List
from enum import Enum

from app.utils.utils import IdGenerator

from .general import PaginatedResponse


class CustomerType(Enum):
    STANDARD = "Standard"
    ANALYST = "Analyst"


class CustomerBase(BaseModel):
    personal_id: Annotated[str, Query(max_length=50)]
    family_name: Annotated[str, Query(max_length=50)]
    middle_name: Annotated[str | None, Query(max_length=50)] = None
    surname: Annotated[str, Query(max_length=50)]
    additional_surname: Annotated[str | None, Query(max_length=50)] = None


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
