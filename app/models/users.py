from pydantic import BaseModel, EmailStr, Field

from app.utils.utils import IdGenerator


# TODO: consider a validator for the email (only apibank are accepted?)
class UserBase(BaseModel):
    mail: EmailStr
    password: str


class UserIn(UserBase):
    pass


class NewUser(UserIn):
    id: int = Field(default_factory=IdGenerator.get_id)


class User(UserBase):
    id: int
