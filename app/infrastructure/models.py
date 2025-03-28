from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.domain.models import PaymentMethod, PaymentStatus


class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    wallets = relationship("Wallet", back_populates="user")
    payments = relationship("Payment", back_populates="user")


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