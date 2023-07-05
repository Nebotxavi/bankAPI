from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from app.constants.constants import EMAIL_REGEX

from app.utils.utils import IdGenerator


class UserBase(BaseModel):
    mail: Annotated[str, Query(min_length=5, regex=EMAIL_REGEX)]
    password: str


class UserIn(UserBase):
    pass


class User(UserBase):
    id: int = Field(default_factory=IdGenerator.get_id)
