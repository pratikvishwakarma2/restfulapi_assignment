# third party
from sqlalchemy.orm import Session

# fastapi
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

# marsdevs
from src.api.services import authentication as ser_authentication
from src.config.database import get_db

router = APIRouter(tags=["Authentication:"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return ser_authentication.login(request, db)
