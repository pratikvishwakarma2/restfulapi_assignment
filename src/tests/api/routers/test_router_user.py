import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import BASE, get_db
from src.main import app
from src.api.models.user import User, Role
from src.api.utils.hash import Hash
from src.config.settings import TEST_DATABASE_URL
from src.config.token import create_access_token

# Create a SQLAlchemy engine for the test database
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    # Create tables
    BASE.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    # Drop tables
    BASE.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_user_create(db):
    response = client.post(
        "/user/",
        json={
            "email": "newuser@example.com",
            "password": "newpassword",
            "role": "Teacher"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"

def test_user_get_by_id(db):
    # Create a test user
    user = User(
        email="testuser@example.com",
        password=Hash.bcrpyt("testpassword"),
        is_active=True,
        role=Role.teacher
    )
    db.add(user)
    db.commit()

    # Create a token for the test user
    access_token = create_access_token(data={"email": user.email, "role": user.role.value})

    # Attempt to get the user by ID with authentication
    response = client.get(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_user_all(db):
    # Create test users
    user1 = User(
        email="user1@example.com",
        password=Hash.bcrpyt("password1"),
        is_active=True,
        role=Role.student
    )
    user2 = User(
        email="user2@example.com",
        password=Hash.bcrpyt("password2"),
        is_active=True,
        role=Role.teacher
    )
    db.add(user1)
    db.add(user2)
    db.commit()

    # Get all users
    response = client.get("/user/all")
    assert response.status_code == 200
    assert len(response.json()["items"]) >= 2

def test_user_delete(db):
    # Create a test user
    user = User(
        email="deleteuser@example.com",
        password=Hash.bcrpyt("deletepassword"),
        is_active=True,
        role=Role.admin
    )
    db.add(user)
    db.commit()

    # Create a token for the test user
    access_token = create_access_token(data={"email": user.email, "role": user.role.value})

    # Delete the user with authentication
    response = client.delete(
        f"/user/{user.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 204

def test_user_reset_password(db):
    # Create a test user
    user = User(
        email="resetuser@example.com",
        password=Hash.bcrpyt("oldpassword"),
        is_active=True,
        role=Role.teacher
    )
    db.add(user)
    db.commit()

    # Create a token for the test user
    access_token = create_access_token(data={"email": user.email, "role": user.role.value})

    # Reset password with authentication
    response = client.post(
        "/user/reset_password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "old_password": "oldpassword",
            "new_password": "newpassword",
            "confirm_password": "newpassword"
        }
    )
    assert response.status_code == 200

def test_user_update_status(db):
    # Create test users
    user1 = User(
        email="statususer1@example.com",
        password=Hash.bcrpyt("password1"),
        is_active=False,
        role=Role.student
    )
    user2 = User(
        email="statususer2@example.com",
        password=Hash.bcrpyt("password2"),
        is_active=False,
        role=Role.teacher
    )
    db.add(user1)
    db.add(user2)
    db.commit()

    # Update user status
    response = client.post(
        "/user/update_user_status",
        params={"ids": [user1.id, user2.id], "status": True}
    )
    assert response.status_code == 200