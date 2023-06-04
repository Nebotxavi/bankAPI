from pydantic import BaseModel

# TODO: to be removed
class DatabaseTest(BaseModel):
    name: str
    test: int