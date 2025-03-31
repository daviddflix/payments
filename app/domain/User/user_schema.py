from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC)) 