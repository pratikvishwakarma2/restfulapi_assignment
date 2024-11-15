# stdlib
from contextlib import asynccontextmanager

# third party
from fastapi_pagination import add_pagination

# fastapi
from fastapi import FastAPI

# marsdevs
from src.config import database, settings
from src.api.models import user as m_user
from src.api.routers import user as r_user, authentication as r_authentication

# user.BASE.metadata.create_all(bind=database.ENGINE)


app = FastAPI(**settings.APP_DESCRIPTION)

m_user.BASE.metadata.create_all(bind=database.ENGINE)

app.include_router(r_user.router)
app.include_router(r_authentication.router)


@app.get("/", tags=["Defaults:"])
async def root():
    return {"message": "Hello FastAPI"}


add_pagination(app)
