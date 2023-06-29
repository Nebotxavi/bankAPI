from pydantic import BaseModel, Field
from enum import Enum
from typing import List

from app.utils.utils import IdGenerator

from .general import ListResponse


class ProductType(Enum):
    BASIC = "Basic"
    PLUS = "Plus"


class ProductBase(BaseModel):
    type: ProductType


class Product(ProductBase):
    id: int


class NewProduct(Product):
    id: int = Field(default_factory=IdGenerator.get_id)


class ProductList(ListResponse):
    data: List[Product]
