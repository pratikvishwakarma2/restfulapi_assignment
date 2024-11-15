import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from src.config.database import BASE, get_db
from src.api.models.user import User, Profile, Role
from src.api.services.user import (
    get_all, get_by_id, create, destroy, update_user_status,
    profile_detail, profile_update_detail, reset_password
)
from src.api.schemas.user import CreateUser, Profile as ProfileSchema, PasswordResetRequest
from src.api.utils.hash import Hash
from src.config.settings import TEST_DATABASE_URL

# Create a SQLAlchemy engine for the test database
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Create tables
    BASE.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    # Drop tables
    BASE.metadata.drop_all(bind=engine)

def test_get_all_users(db):
    user1 = User(email="user1@example.com", password=Hash.bcrpyt("password1"), role=Role.teacher)
    user2 = User(email="user2@example.com", password=Hash.bcrpyt("password2"), role=Role.student)
    db.add(user1)
    db.add(user2)
    db.commit()

    users = get_all(db)
    assert len(users) == 2

def test_get_user_by_id(db):
    user = User(email="user@example.com", password=Hash.bcrpyt("password"), role=Role.teacher)
    db.add(user)
    db.commit()

    fetched_user = get_by_id(user.id, db)
    assert fetched_user.email == "user@example.com"

def test_create_user(db):
    request = CreateUser(email="newuser@example.com", password="newpassword", role=Role.teacher)
    new_user = create(db, request)
    assert new_user.email == "newuser@example.com"

def test_destroy_user(db):
    user = User(email="deleteuser@example.com", password=Hash.bcrpyt("password"), role=Role.admin)
    db.add(user)
    db.commit()

    response = destroy(user.id, db)
    assert response["message"] == f"user with id `{user.id}` is deleted!"

def test_update_user_status(db):
    user = User(email="statususer@example.com", password=Hash.bcrpyt("password"), role=Role.student, is_active=False)
    db.add(user)
    db.commit()

    response = update_user_status([user.id], True, db)
    assert response["message"] == "status update successfully!"
    assert db.query(User).filter(User.id == user.id).first().is_active is True

def test_profile_detail(db):
    # Create and commit the user first
    user = User(email="profileuser@example.com", password=Hash.bcrpyt("password"), role=Role.teacher)
    db.add(user)
    db.commit()  # Commit to ensure user_id is generated

    # Now create the profile with the committed user_id
    profile = Profile(user_id=user.id, first_name="John", last_name="Doe")
    db.add(profile)
    db.commit()

    user_profile = profile_detail(user.id, db)
    assert user_profile.first_name == "John"