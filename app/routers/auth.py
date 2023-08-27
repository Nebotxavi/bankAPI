from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.auth.oauth2 import create_access_token
from app.exceptions.general_exceptions import ResourceNotFound
from app.models.auth import LoginResponse
from app.storage.storage import Storage, StorageAccess
from app.utils.utils import Crypt

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=LoginResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), client: Storage=Depends(StorageAccess.get_db)):
    try:
        user = client.get_user(
            mail=user_credentials.username)  # username == mail

        if not Crypt.verify(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

        access_token = create_access_token(data={'user_id': user.id})

        return {'access_token': access_token, 'token_type': 'bearer'}

    except ResourceNotFound:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
