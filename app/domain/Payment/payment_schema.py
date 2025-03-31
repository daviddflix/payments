from datetime import datetime, UTC
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    BITCOIN = "bitcoin"
    BANK_TRANSFER = "bank_transfer"


class Payment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    amount: float
    currency: str
    status: PaymentStatus
    payment_method: PaymentMethod
    transaction_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC)) 