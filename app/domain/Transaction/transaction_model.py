from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.domain.payment.payment_schema import PaymentMethod, PaymentStatus


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(PGUUID, primary_key=True, default=uuid4)
    wallet_id = Column(PGUUID, ForeignKey("wallets.id"))
    amount = Column(Float)
    currency = Column(String)
    status = Column(Enum(PaymentStatus))
    payment_method = Column(Enum(PaymentMethod))
    transaction_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    wallet = relationship("Wallet", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction", uselist=False)
