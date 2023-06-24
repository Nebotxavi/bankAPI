from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional, List

# TODO: to be removed
class Test(BaseModel):
    name: str
    test: int

M = TypeVar('M')

class ListResponse(GenericModel, Generic[M]):
    data: List[M]

class PaginatedResponse(ListResponse):
    count: Optional[int] = None
    total_pages: Optional[int] = None

