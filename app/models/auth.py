from pydantic import BaseModel


class TokenData(BaseModel):
    id: int

class LoginResponse(BaseModel):
    access_token: str
    token_type: str