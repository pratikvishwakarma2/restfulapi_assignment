# stdlib
from typing import Optional

# third party
from pydantic import Field, BaseModel

# marsdevs
from src.api.models import user as m_user


class Profile(BaseModel):
    # id: int
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[m_user.Gender]
    bio: Optional[str]

    class Config:
        from_attributes = True
        title = "Profile Model"
        extra = "ignore"
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                # "id": 1,
                "first_name": "user",
                "last_name": "user2",
                "gender": "Male",
                "bio": "Some description",
            }
        }


class User(BaseModel):
    id: int
    email: str
    password: str = Field(exclude=True)
    is_active: bool
    role: m_user.Role
    profile: Optional[Profile]

    class Config:
        # use_enum_values = True
        from_attributes = True
        title = "User Model"
        extra = "ignore"
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "role": "Teacher",
            }
        }


class CreateUser(BaseModel):
    email: str
    password: str
    role: m_user.Role

    class Config:
        # use_enum_values = True
        from_attributes = True
        title = "Create User Model"
        extra = "ignore"
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword",
                "role": "Teacher",
            }
        }


class UserPass(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
        title = "Reset User Password Model"
        extra = "ignore"
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yournewpassword",
            }
        }

class PasswordResetRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    class Config:
        from_attributes = True
        title = "Reset User Password Model"
        extra = "ignore"
        str_strip_whitespace = True
        json_schema_extra = {
            "example": {
                "old_password": "currentpassword",
                "new_password": "newsecurepassword",
                "confirm_password": "newsecurepassword",
            }
        }