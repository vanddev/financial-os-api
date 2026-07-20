from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.core.database import Base


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), nullable=False)
    asset_type = Column(String(50), nullable=True)
    quantity = Column(Numeric(18, 6), nullable=False)
    average_price = Column(Numeric(18, 6), nullable=False)
    current_price = Column(Numeric(18, 6), nullable=True)
    broker = Column(String(120), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
