# stdlib
import enum

# third party
from sqlalchemy import Enum, Text, Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

# marsdevs
from src.config.database import BASE

from .mixins import Timestamp


class Role(enum.Enum):
    teacher = "Teacher"
    student = "Student"
    admin = "Admin"


class Gender(enum.Enum):
    male = "Male"
    female = "Female"
    others = "Others"


class User(Timestamp, BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Role, name="role"))

    profile = relationship("Profile", back_populates="owner", uselist=False, cascade="all, delete-orphan")


class Profile(Timestamp, BASE):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    bio = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="profile", single_parent=True)
