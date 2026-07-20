from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String(8), nullable=False)
    locale = Column(String(20), nullable=True)
    timezone = Column(String(50), nullable=True)
    family_name = Column(String(120), nullable=True)
    emergency_fund_target = Column(Numeric(14, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
