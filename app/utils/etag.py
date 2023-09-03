import json
import hashlib
from typing import Any, Callable
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

def get_etag(items: list[BaseModel]):
    individual_etags = []

    for item in items:
        stock_json = json.dumps(jsonable_encoder(item.model_dump()), sort_keys=True)
        etag = hashlib.sha1(stock_json.encode()).hexdigest()
        individual_etags.append(etag)

    # Combine the individual ETags into a single ETag for the list
    combined_etag = hashlib.sha1("".join(individual_etags).encode()).hexdigest()

    return combined_etag


def provide_with_etag(func: Callable[..., list]) -> tuple[str, list]:
    items = func()
    etag = get_etag(items)

    return (etag, items)