from datetime import datetime
from typing import Optional

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from practice.mvc.models.base import (
    TimeStampedModel,
)
from practice.mvc.models.userModel import UserRead


class Product(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float

    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="products")


class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ProductRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner: Optional[UserRead] = None

    class Config:
        from_attributes = True
