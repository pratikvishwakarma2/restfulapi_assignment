# third party
from sqlalchemy.orm import Session

# fastapi
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# marsdevs
from src.config import token
from src.api.models import user as m_user
from src.api.schemas import token as s_token
from src.api.utils.hash import Hash


def login(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(m_user.User).filter(m_user.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials",
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Password",
        )

    data = {"email": user.email, "role": user.role.value}
    print(f"{data = }")
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"email": user.email, "role": user.role.value},
        #   expires_delta=access_token_expires
    )
    return s_token.Token(access_token=access_token, token_type="bearer")
