from sqlalchemy import (
    JSON,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint(
            "idempotency_key",
            name="uq_transactions_idempotency_key",
        ),
        CheckConstraint(
            "(idempotency_key IS NULL AND request_hash IS NULL) OR "
            "(idempotency_key IS NOT NULL AND request_hash IS NOT NULL)",
            name="ck_transactions_idempotency_pair",
        ),
        CheckConstraint(
            "amount > 0",
            name="ck_transactions_amount_positive",
        ),
        CheckConstraint(
            "account_id IS NULL OR credit_card_id IS NULL",
            name="ck_transactions_single_source",
        ),
        CheckConstraint(
            "payment_method != 'credit_card' OR "
            "(credit_card_id IS NOT NULL AND account_id IS NULL)",
            name="ck_transactions_credit_card_source",
        ),
        CheckConstraint(
            "payment_method NOT IN "
            "('debit_card', 'pix', 'bank_transfer', 'automatic_debit') OR "
            "(account_id IS NOT NULL AND credit_card_id IS NULL)",
            name="ck_transactions_account_source",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    idempotency_key = Column(String(255), nullable=True)
    request_hash = Column(String(64), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    credit_card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=True)
    description = Column(String(255), nullable=True)
    amount = Column(Numeric(14, 2), nullable=False)
    transaction_type = Column(String(30), nullable=False)
    payment_method = Column(String(50), nullable=True)
    status = Column(String(30), nullable=True)
    transaction_date = Column(DateTime, nullable=False)
    competency_date = Column(DateTime, nullable=True)
    installment_number = Column(Integer, nullable=True)
    installment_total = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    account = relationship("Account")
    category = relationship("Category")
    subcategory = relationship("Subcategory")
    credit_card = relationship("CreditCard")
