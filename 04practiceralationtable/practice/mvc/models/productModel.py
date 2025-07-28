from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float

    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="products")


class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    user_id: int  # foreign key reference to User

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class UserRead(SQLModel):
    id: int
    full_name: str
    email: str
    class Config:
        orm_mode = True
class ProductRead(SQLModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    owner: Optional[UserRead] = None
    class Config:
        orm_mode = True