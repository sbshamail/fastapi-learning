from practice.mvc.models.base import TimeStampedModel
from pydantic import EmailStr,BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
class Role(str, Enum):
    admin = "admin"
    user = "user"


class User(TimeStampedModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: EmailStr
    password: str
    is_active: bool = True
    gender:Optional[str]=None
    age: Optional[int] = None
     # Relationships
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")
    products: List["Product"] = Relationship(back_populates="owner")


class RegisterUser(SQLModel):
    full_name: str
    email: EmailStr
    password: str
   

class UserRead(SQLModel):
    id: int
    full_name: str
    email: EmailStr
    role: Role

class LoginRequest(BaseModel):
    email: EmailStr
    password: str