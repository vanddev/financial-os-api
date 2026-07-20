from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.core.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    loan_type = Column(String(80), nullable=True)
    original_amount = Column(Numeric(14, 2), nullable=False)
    current_balance = Column(Numeric(14, 2), nullable=False)
    interest_rate = Column(Numeric(6, 4), nullable=True)
    total_installments = Column(Integer, nullable=True)
    paid_installments = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
