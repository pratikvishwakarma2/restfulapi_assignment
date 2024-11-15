import pytest
from datetime import timedelta
from jose import jwt, JWTError
from unittest.mock import patch
from src.config.token import create_access_token, verify_token, SECRET_KEY, ALGORITHM
from src.api.schemas.token import TokenData
from fastapi import HTTPException, status

def test_create_access_token():
    data = {"email": "test@example.com"}
    token = create_access_token(data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["email"] == "test@example.com"
    assert "exp" in payload

def test_create_access_token_with_expiry():
    data = {"email": "test@example.com"}
    expires = timedelta(minutes=5)
    token = create_access_token(data, expires)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["email"] == "test@example.com"
    assert "exp" in payload

def test_verify_token_success():
    data = {"email": "test@example.com"}
    token = create_access_token(data)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    assert token_data.email == "test@example.com"

def test_verify_token_failure():
    invalid_token = "invalidtoken"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    with pytest.raises(HTTPException) as exc_info:
        verify_token(invalid_token, credentials_exception)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"