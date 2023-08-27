from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, computed_field
from app.constants.constants import EMAIL_REGEX

from app.utils.utils import IdGenerator


class UserBase(BaseModel):
    mail: Annotated[str, Query(min_length=5, pattern=EMAIL_REGEX)]
    password: str


class UserIn(UserBase):
    
    @computed_field
    @property
    def id(self) -> int:
        return IdGenerator.get_id()


class User(UserBase):
    id: int
