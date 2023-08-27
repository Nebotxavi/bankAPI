from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Any

# TODO: to be removed


class Test(BaseModel):
    name: str
    test: int


M = TypeVar('M')


class ListResponse(BaseModel, Generic[M]):
    data: list[M]


class PaginatedResponse(ListResponse):
    count: int | None = None
    total_pages: int | None = None
    next_page: str | None = None
    previous_page: str | None = None
