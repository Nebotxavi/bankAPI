from fastapi import APIRouter, Depends, Header, Response

from app.auth.oauth2 import get_current_user
from app.models.stock import Stock

from app.storage.storage import Storage, StorageAccess
from app.utils.etag import provide_with_etag

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.get("/", response_model=list[Stock])
def get_stocks(
    response: Response,
    client: Storage = Depends(StorageAccess.get_db),
    if_none_match: str | None = Header(default=None),
    current_user: int = Depends(get_current_user),
):
    (etag, stocks) = provide_with_etag(client.get_stocks)

    
    if if_none_match == etag:
        return Response(status_code=304)

    response.headers['if_none_match'] = etag
    return stocks
