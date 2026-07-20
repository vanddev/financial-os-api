from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.core.database import Base


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    issuer = Column(String(120), nullable=True)
    last_four = Column(String(4), nullable=True)
    limit = Column(Numeric(12, 2), nullable=False, default=0)
    closing_day = Column(Integer, nullable=True)
    due_day = Column(Integer, nullable=True)
    color = Column(String(20), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
