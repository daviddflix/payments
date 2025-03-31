from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(PGUUID, primary_key=True, default=uuid4)
    user_id = Column(PGUUID, ForeignKey("users.id"))
    address = Column(String, unique=True, index=True)
    private_key = Column(String)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="BTC")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")