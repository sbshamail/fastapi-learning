from enum import Enum
from typing import (
    Annotated,
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    EmailStr,
    StringConstraints,
    model_validator,
)
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from practice.mvc.models.base import (
    TimeStampedModel,
)
from practice.mvc.models.roleModel import (
    Role,
)


class User(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: EmailStr
    password: str
    phone: Annotated[
        Optional[str],
        StringConstraints(pattern=r"^\d{11}$"),
        Field(description="User's login name"),
    ]
    is_active: bool = True
    gender: Optional[str] = None
    age: Optional[int] = None
    # Relationships
    role_id: Optional[int] = Field(
        default=None,
        foreign_key="user_role.id",
    )
    role: Optional["Role"] = Relationship(back_populates="users")
    products: List["Product"] = Relationship(back_populates="owner")


class RegisterUser(SQLModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="before")
    def check_password_match(cls, values):
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values


class RoleReadForUser(SQLModel):
    id: int
    title: str
    permissions: list[str]


class UserRead(SQLModel):
    id: int
    full_name: str
    email: EmailStr
    role: Optional[RoleReadForUser] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
