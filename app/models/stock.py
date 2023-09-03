from pydantic import BaseModel
from datetime import datetime as Datetime


class Stock(BaseModel):
    name: str
    value: float
    last_update: Datetime | None = None
    id: int

    def update_last_date(self) -> None:
        self.last_update = Datetime.now()