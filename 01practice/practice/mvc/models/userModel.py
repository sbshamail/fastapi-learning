from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    is_active: bool = True


class UserCreate(SQLModel):
    full_name: str
    email: str