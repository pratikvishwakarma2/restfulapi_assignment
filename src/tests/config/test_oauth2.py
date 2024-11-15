import pytest
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from unittest.mock import patch
from src.config.oauth2 import get_current_user

# Mock token verification function
def mock_verify_token_success(token, credentials_exception):
    return {"user_id": 1, "email": "test@example.com"}

def mock_verify_token_failure(token, credentials_exception):
    raise credentials_exception

@pytest.fixture
def token():
    return "testtoken"

def test_get_current_user_success(token):
    with patch("src.config.oauth2.verify_token", side_effect=mock_verify_token_success):
        user = get_current_user(token)
        assert user["email"] == "test@example.com"

def test_get_current_user_failure(token):
    with patch("src.config.oauth2.verify_token", side_effect=mock_verify_token_failure):
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc_info.value.detail == "Could not validate credentials"