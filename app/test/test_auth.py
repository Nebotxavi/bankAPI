import pytest
from fastapi import status
from app.models.users import User


def test_login(test_user: User, client):
    body = {"username": test_user.mail, "password": "testpassword1"}
    res = client.post("/login", data=body)

    content = res.json()

    assert content.get("access_token")
    assert content.get("token_type")
    assert res.status_code == status.HTTP_200_OK


def test_login_with_wrong_user(client):
    body = {"username": "fake_user", "password": "fake_password"}

    res = client.post("/login", data=body)

    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_login_with_wrong_password(test_user: User, client):
    body = {"username": test_user.mail, "password": "fake_password"}

    res = client.post("/login", data=body)

    assert res.status_code == status.HTTP_403_FORBIDDEN
