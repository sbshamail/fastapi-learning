from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    is_active: bool = True
    gender:str
    age: Optional[int] = None
    products: List["Product"] = Relationship(back_populates="owner")



class UserCreate(SQLModel):
    full_name: str
    email: str
    gender:str
    age: Optional[int] = None