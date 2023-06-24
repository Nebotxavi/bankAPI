from pydantic import BaseModel
from enum import Enum
from typing import List

from .general import ListResponse


class ProductType(Enum):
    BASIC = "Basic"
    PLUS = "Plus"


class ProductBase(BaseModel):
    id: str
    type: ProductType


class Product(ProductBase):
    pass

class ProductList(ListResponse):
    data: List[Product]