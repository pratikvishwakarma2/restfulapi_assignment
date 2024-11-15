import pytest
from pydantic import ValidationError
from src.api.schemas.token import Token, TokenData

def test_token_schema():
    data = {
        "access_token": "someaccesstoken",
        "token_type": "bearer"
    }
    token = Token(**data)
    assert token.access_token == "someaccesstoken"
    assert token.token_type == "bearer"

def test_token_schema_missing_fields():
    data = {
        "access_token": "someaccesstoken"
    }
    with pytest.raises(ValidationError):
        Token(**data)

def test_token_data_schema():
    data = {
        "email": "user@example.com",
        "role": "Teacher"
    }
    token_data = TokenData(**data)
    assert token_data.email == "user@example.com"
    assert token_data.role == "Teacher"

def test_token_data_schema_optional_fields():
    data = {}
    token_data = TokenData(**data)
    assert token_data.email is None
    assert token_data.role is None