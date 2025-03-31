from datetime import datetime, UTC
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Wallet(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    address: str
    private_key: str
    balance: float = 0.0
    currency: str = "BTC"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC)) 