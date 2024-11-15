import pytest
from pydantic import ValidationError
from src.api.schemas.user import User, CreateUser, UserPass, PasswordResetRequest, Profile
from src.api.models.user import Role, Gender

def test_create_user_schema():
    data = {
        "email": "user@example.com",
        "password": "yourpassword",
        "role": Role.teacher
    }
    user = CreateUser(**data)
    assert user.email == "user@example.com"
    assert user.role == Role.teacher

def test_create_user_schema_invalid_role():
    data = {
        "email": "user@example.com",
        "password": "yourpassword",
        "role": "InvalidRole"
    }
    with pytest.raises(ValidationError):
        CreateUser(**data)

def test_user_schema():
    data = {
        "id": 1,
        "email": "user@example.com",
        "password": "yourpassword",
        "is_active": True,
        "role": Role.teacher,
        "profile": {
            "first_name": "John",
            "last_name": "Doe",
            "gender": Gender.male,
            "bio": "A short bio"
        }
    }
    user = User(**data)
    assert user.email == "user@example.com"
    assert user.role == Role.teacher
    assert user.profile.first_name == "John"

def test_user_pass_schema():
    data = {
        "email": "user@example.com",
        "password": "yournewpassword"
    }
    user_pass = UserPass(**data)
    assert user_pass.email == "user@example.com"

def test_password_reset_request_schema():
    data = {
        "old_password": "currentpassword",
        "new_password": "newsecurepassword",
        "confirm_password": "newsecurepassword"
    }
    password_reset = PasswordResetRequest(**data)
    assert password_reset.new_password == "newsecurepassword"

def test_profile_schema():
    data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "gender": Gender.female,
        "bio": "Another short bio"
    }
    profile = Profile(**data)
    assert profile.first_name == "Jane"
    assert profile.gender == Gender.female