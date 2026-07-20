from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
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
