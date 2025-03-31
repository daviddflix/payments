from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.domain.payment.payment_schema import PaymentMethod, PaymentStatus

class Payment(Base):
    __tablename__ = "payments"

    id = Column(PGUUID, primary_key=True, default=uuid4)
    user_id = Column(PGUUID, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String)
    status = Column(Enum(PaymentStatus))
    payment_method = Column(Enum(PaymentMethod))
    transaction_id = Column(PGUUID, ForeignKey("transactions.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="payments")
    transaction = relationship("Transaction", back_populates="payment") 