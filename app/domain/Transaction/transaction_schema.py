from datetime import datetime, UTC
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.payment.payment_schema import PaymentMethod, PaymentStatus


class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    wallet_id: UUID
    amount: float
    currency: str
    status: PaymentStatus
    payment_method: PaymentMethod
    transaction_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC)) 