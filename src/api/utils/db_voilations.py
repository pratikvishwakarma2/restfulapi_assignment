# third party
from psycopg2.errors import UniqueViolation

# fastapi
from fastapi import HTTPException, status


def handle_integrity_error(error: Exception):
    if isinstance(error.orig, UniqueViolation):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource already exists.",
        )
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=error,
    )
