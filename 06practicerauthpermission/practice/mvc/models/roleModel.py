from dataclasses import Field
from practice.mvc.models.base import TimeStampedModel
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Role(TimeStampedModel, table=True):
    id = Optional[int] = Field(default=None, primary_key=True)
    name = str
    permissions: List[str]
    users: List["User"] = Relationship(back_populates="role")   
