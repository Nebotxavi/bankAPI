from pydantic import BaseModel, Field, computed_field
from enum import Enum

from app.utils.utils import IdGenerator

from .general import ListResponse


class ProductType(Enum):
    BASIC = "Basic"
    PLUS = "Plus"


class ProductBase(BaseModel):
    type: ProductType


class Product(ProductBase):
    id: int


class ProductIn(ProductBase):
    @computed_field
    @property
    def id(self) -> int:
        return IdGenerator.get_id()


class ProductListCollection(ListResponse):
    data: list[Product]
