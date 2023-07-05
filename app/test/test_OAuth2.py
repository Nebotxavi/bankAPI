import pytest
from fastapi import HTTPException, status
from app.auth.oauth2 import create_access_token, _verify_access_token, get_current_user
from app.config import settings
from app.models.users import User
from jose.jwt import decode


def test_create_access_token(test_user: User):

    token = create_access_token(data={'user_id': test_user.id})

    payload = decode(token, settings.secret_key)
    assert payload
    assert test_user.id == payload['user_id']
    assert payload.get('exp')


def test_verify_access_token(test_user: User, token: str):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token_data = _verify_access_token(token, exception)

    assert token_data
    assert int(token_data.id) == test_user.id


def test_verify_access_token_with_modified_token(token: str):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Could not validate the credentials", headers={"WWW-Authenticate": "Bearer"})

    modified_token = token + '8888888'

    with pytest.raises(HTTPException) as exc_info:
        _verify_access_token(modified_token, exception)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate the credentials"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_get_current_user(test_user: User, token: str, storage):
    user = get_current_user(token, storage)

    assert user
    assert user.password
    assert user.mail == test_user.mail
    assert user.id == test_user.id


def test_get_current_user_with_wrong_user(test_user: User, storage):
    token = create_access_token(data={'user_id': test_user.id + 1})

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token, storage)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
