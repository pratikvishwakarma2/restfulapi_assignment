# stdlib
from typing import List

# third party
from sqlalchemy.orm import Session
from fastapi_filters import FilterValues, create_filters, create_filters_from_model
from fastapi_pagination import Page, Params, paginate
from fastapi_filters.ext.sqlalchemy import apply_filters

# fastapi
from fastapi import Path, Query, Depends, APIRouter, status

from src.api.models.user import User
# marsdevs
from src.api.schemas import user as s_user
from src.api.services import user as ser_user
from src.api.services.user import get_current_user
from src.config.database import get_db

# from api.filters.users import UserFilter


# from fastapi_filter.contrib.sqlalchemy import apply_filters

router = APIRouter(prefix="/user", tags=["Users:"])


@router.get("/all", response_model=Page[s_user.User])
def user_all(
    db: Session = Depends(get_db),
    # filters: FilterValues = Depends(create_filters_from_model(s_user.User)),
    params: Params = Depends(),
    # current_user: s_user.User = Depends(get_current_user),
):
    # print(f"{current_user = }")
    users = ser_user.get_all(db)
    # users_filtered = user_filter.filter(users)
    # users_filtered = apply_filters(users, filters)
    return paginate(users, params)


@router.get("/{id}", response_model=s_user.User)
def user_get_by_id(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ser_user.get_by_id(current_user.id, db)


@router.post("/", response_model=s_user.User)
def user_create(request: s_user.CreateUser, db: Session = Depends(get_db)):
    return ser_user.create(db, request)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def user_destroy(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ser_user.destroy(current_user.id, db)


@router.post("/reset_password", status_code=status.HTTP_200_OK)
def user_reset_password(request: s_user.PasswordResetRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ser_user.reset_password(db, current_user, request)


@router.post("/update_user_status", status_code=status.HTTP_200_OK)
def user_update_status(
    db: Session = Depends(get_db),
    ids: List[int] = Query([], description="List of User ID to change its status"),
    status: bool = Query(False, description="Active/Inactive status of user"),
):
    return ser_user.update_user_status(ids, status, db)


# PROFILE SECTION
@router.get("/{id}/profile", response_model=s_user.Profile)
def user_get_profile_detail(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ser_user.profile_detail(current_user.id, db)


@router.post("/{id}/profile", response_model=s_user.Profile)
def user_update_profile_detail(
    request: s_user.Profile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ser_user.profile_update_detail(current_user.id, request, db)
