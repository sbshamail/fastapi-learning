from dataclasses import Field
from typing import List, Optional

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

from practice.mvc.models.base import (
    TimeStampedModel,
)


class Role(TimeStampedModel, table=True):
    __tablename__ = "user_role"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column_kwargs={"unique": True})
    permissions: list[str] = Field(
        default_factory=list,
        sa_type=JSON,
    )
    users: List["User"] = Relationship(back_populates="role")


class RoleCreate(SQLModel):
    title: str
    permissions: list[str]


class RoleUpdate(SQLModel):
    title: Optional[str] = None
    permissions: Optional[List[str]] = None


class RoleRead(SQLModel):
    id: int
    title: str
    permissions: list[str]

    class Config:
        orm_mode = True
