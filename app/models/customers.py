from fastapi import Query
from pydantic import BaseModel, computed_field
from typing import Annotated
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
    id: int


class CustomerIn(CustomerDetail):
    @computed_field
    @property
    def id(self) -> int:
        return IdGenerator.get_id()


class CustomerBasic(CustomerBase):
    id: int
    href: str | None = None


class CustomerPagination(PaginatedResponse):
    data: list[CustomerBasic]
