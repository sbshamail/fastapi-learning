from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class TimeStampedModel(SQLModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
