# FastAPI's routing module, dependency injection, and HTTP exception class
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from sqlalchemy.orm import selectinload
from typing import Any, Dict, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
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
from practice.lib.dependencies import GetSession
from practice.lib.helpers.utility import Print
from practice.lib.operation import listop
from practice.mvc.models.userModel import (
    User,
    UserRead,
)

# Create a router with prefix `/user` and group tag `user`
router = APIRouter(prefix="/user", tags=["user"])


# ✅ READ ALL
@router.get("/all")  # no response_model
def get_users(
    session: GetSession,
    dateRange: Optional[
        str
    ] = None,  # JSON string like '["created_at", "01-01-2025", "01-12-2025"]'
    numberRange: Optional[str] = None,  # JSON string like '["amount", "0", "100000"]'
    searchTerm: str = None,
    columnFilters: Optional[str] = Query(
        None
    ),  # e.g. '[["name","car"],["description","product"]]'
    page: int = None,
    skip: int = 0,
    limit: int = Query(10, ge=1, le=100),
):

    filters = {
        "searchTerm": searchTerm,
        "columnFilters": columnFilters,
        "dateRange": dateRange,
        "numberRange": numberRange,
    }
    searchFields = [
        "name",
        "description",
        "owner.full_name",
        "owner.email",
    ]
    result = listop(
        session=session,
        Model=User,
        join_options=[selectinload(User.role)],
        searchFields=searchFields,
        filters=filters,
        skip=skip,
        page=page,
        limit=limit,
    )

    if not result["data"]:
        return api_response(404, "No products found")
    Print(result, "Products")
    # Convert each SQLModel Product instance into a UserRead Pydantic model
    # This ensures relationships like `Role` are included in the serialized output
    product_list = [UserRead.model_validate(prod) for prod in result["data"]]

    return api_response(
        200,
        "Products found",
        product_list,
        result["total"],
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
