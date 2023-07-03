from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, List, TypedDict, Any

# TODO: to be removed


class Test(BaseModel):
    name: str
    test: int


M = TypeVar('M')


class ListResponse(GenericModel, Generic[M]):
    data: List[M]


class PaginatedResponse(ListResponse):
    count: int | None = None
    total_pages: int | None = None
    next_page: str | None = None
    previous_page: str | None = None
