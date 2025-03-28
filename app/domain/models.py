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


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Wallet(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    address: str
    private_key: str
    balance: float = 0.0
    currency: str = "BTC"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


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