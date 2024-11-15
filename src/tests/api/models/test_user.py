import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.models.user import User, Profile, Role, Gender
from src.config.database import BASE
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

def test_create_user(db):
    user = User(
        email="test@example.com",
        password="hashedpassword",
        is_active=True,
        role=Role.teacher
    )
    db.add(user)
    db.commit()
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == Role.teacher

def test_create_profile(db):
    user = User(
        email="test2@example.com",
        password="hashedpassword",
        is_active=True,
        role=Role.student
    )
    db.add(user)
    db.commit()

    profile = Profile(
        first_name="John",
        last_name="Doe",
        gender=Gender.male,
        bio="A short bio",
        owner=user
    )
    db.add(profile)
    db.commit()
    assert profile.id is not None
    assert profile.first_name == "John"
    assert profile.owner.email == "test2@example.com"

def test_user_profile_relationship(db):
    user = User(
        email="test3@example.com",
        password="hashedpassword",
        is_active=True,
        role=Role.admin
    )
    db.add(user)
    db.commit()

    profile = Profile(
        first_name="Jane",
        last_name="Doe",
        gender=Gender.female,
        bio="Another short bio",
        owner=user
    )
    db.add(profile)
    db.commit()

    assert user.profile is not None
    assert user.profile.first_name == "Jane"
    assert profile.owner.email == "test3@example.com"

def test_unique_email_constraint(db):
    user1 = User(
        email="unique@example.com",
        password="hashedpassword",
        is_active=True,
        role=Role.teacher
    )
    db.add(user1)
    db.commit()

    user2 = User(
        email="unique@example.com",
        password="hashedpassword",
        is_active=True,
        role=Role.student
    )
    db.add(user2)
    with pytest.raises(Exception):
        db.commit()

def test_cascade_delete_user(db):
    user = User(
        email="test4@example.com",
        password="hashedpassword",
        is_active=True,
        role=Role.admin
    )
    db.add(user)
    db.commit()

    profile = Profile(
        first_name="Alice",
        last_name="Smith",
        gender=Gender.others,
        bio="Yet another bio",
        owner=user
    )
    db.add(profile)
    db.commit()

    db.delete(user)
    db.commit()

    assert db.query(Profile).filter(Profile.user_id == user.id).first() is None