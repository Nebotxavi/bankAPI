from pydantic import BaseModel

# TODO: to be removed
class Test(BaseModel):
    name: str
    test: int
    message: str