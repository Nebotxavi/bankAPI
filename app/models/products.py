from pydantic import BaseModel
from enum import Enum


class ProductType(Enum):
    BASIC = "Basic"
    PLUS = "Plus"


class ProductBase(BaseModel):
    id: str
    type: ProductType


class Product(ProductBase):
    pass
