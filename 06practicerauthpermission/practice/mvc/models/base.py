from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
class TimeStampedModel(SQLModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None