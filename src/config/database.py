from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.settings import DATABASE_URL

SQLALCHEMY_DATABASE_URL = DATABASE_URL

ENGINE = create_engine(
    SQLALCHEMY_DATABASE_URL,
)


SESSION_LOCAL = sessionmaker(
    bind=ENGINE,
    autocommit=False,
    autoflush=False
)

BASE = declarative_base()


# DB Utilities
def get_db():
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()
