# stdlib
from typing import List

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
# third party
from sqlalchemy.orm import Session, joinedload

# fastapi
from fastapi import HTTPException, status, Depends

from src.api.models.user import User
from src.api.schemas.user import PasswordResetRequest
# marsdevs
from src.api.utils import hash
from src.api.models import user as m_user
from src.api.schemas import user as s_user
from src.config import settings
from src.config.database import get_db


# from api.utils.db_voilations import handle_integrity_errors


def get_all(db: Session):
    users = db.query(m_user.User).all()
    # users = db.query(m_user.User).options(joinedload(m_user.User.profile)).all()
    return users


def get_by_id(id: int, db: Session):
    user = db.query(m_user.User).filter(m_user.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id `{id}` not found",
        )
    return user


def create(db: Session, request: s_user.User):
    print(f"{request.model_dump(exclude={'id'}) = }")
    new_user = m_user.User(**request.model_dump(exclude={"id"}))
    new_user.password = hash.Hash.bcrpyt(request.password)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="something went wrong..."
        )
        # handle_integrity_errors(e)

    user_profile = m_user.Profile(user_id=new_user.id)
    db.add(user_profile)
    db.commit()
    return new_user


def destroy(id: int, db: Session):
    # Fetch the user and related profile
    user = db.query(m_user.User).filter(m_user.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id `{id}` not found",
        )
    
    # Delete the related profile if it exists
    if user.profile:
        db.delete(user.profile)
    
    # Delete the user
    db.delete(user)
    db.commit()
    return {"message": f"user with id `{id}` is deleted!"}


def update_user_status(ids: List[int], new_status: bool, db: Session):
    users = db.query(m_user.User).filter(m_user.User.id.in_(ids)).all()

    # Check for missing user
    found_user = {user.id for user in users}
    missing_user = list(set(ids) - found_user)
    if missing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User Not found for IDS: {missing_user}",
        )

    db.query(m_user.User).filter(m_user.User.id.in_(ids)).update(
        {m_user.User.is_active: new_status},
        synchronize_session=False,
    )

    db.commit()
    return {"message": "status update successfully!", "ids": ids}


# def reset_password(db: Session, request: s_user.UserPass):
#     new_pass = request.model_dump()
#     user = db.query(m_user.User).filter(m_user.User.email == new_pass["email"]).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"user with email `{new_pass['email']}` not found",
#         )
#     user.password = hash.Hash.bcrpyt(new_pass["password"])
#     db.commit()
#     db.refresh(user)
#     return {"message": "Password update successfully!"}


def profile_detail(id: int, db: Session):
    user_profile = db.query(m_user.Profile).filter(m_user.Profile.user_id == id).first()
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id `{id}` not found",
        )
    return user_profile


def profile_update_detail(id: int, request: s_user.Profile, db: Session):
    user = db.query(m_user.User).filter(m_user.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"user with id `{id}` not found",
        )
    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(user.profile, key, value)

    db.commit()
    db.refresh(user.profile)
    return user.profile


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials user not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def reset_password(db: Session, current_user, request: PasswordResetRequest):
    print(current_user)
    if not verify_password(request.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match",
        )

    current_user.password = hash_password(request.new_password)
    db.commit()
    db.refresh(current_user)
    return {"message": "Password updated successfully!"}