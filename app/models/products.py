from pydantic import BaseModel
from enum import Enum

class ProductType(Enum):
    BASIC = "Basic"
    PLUS = "Plus"

class ProductBase(BaseModel):
    id: int
    type: ProductType

class Product(ProductBase):
    pass
