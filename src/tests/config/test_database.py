import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import BASE, get_db, SQLALCHEMY_DATABASE_URL

# Create a SQLAlchemy engine for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
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

def test_database_connection():
    # Test if the engine can connect to the database
    connection = engine.connect()
    assert connection is not None
    connection.close()

def test_get_db(db):
    # Test the get_db utility
    db_instance = next(get_db())
    assert db_instance is not None
    db_instance.close()