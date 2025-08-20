# FastAPI's routing module, dependency injection, and HTTP exception class
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import Any, Dict

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

# SQLModel's session and query builder
from sqlmodel import Session, select

# Your custom user model and schema
from practice.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Your own standard response formatter
from practice.lib import api_response

# Session provider (dependency injection for DB access)
from practice.lib.db import get_session
from practice.mvc.models.userModel import (
    User,
)

# Create a router with prefix `/user` and group tag `user`
router = APIRouter(prefix="/user", tags=["user"])


# ✅ READ ALL
@router.get("/all")  # no response_model
def get_users(
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()  # SELECT * FROM user
    if not users or len(users) == 0:
        return api_response(404, "User not found")

    return api_response(
        200,
        "Users fetched",
        users,
        len(users),
    )


# ✅ READ ONE
@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)  # Like findById
    if not user:
        # raise HTTPException(status_code=404, detail="User not found")
        return api_response(404, "User not found")
    return api_response(200, "User Found", user)


# ✅ DELETE
@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        return api_response(404, "User not found")

    session.delete(user)
    session.commit()
    return api_response(404, f"User {user_id} deleted")
