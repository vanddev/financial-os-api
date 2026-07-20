from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    asset_type = Column(String(80), nullable=True)
    purchase_value = Column(Numeric(14, 2), nullable=False)
    current_value = Column(Numeric(14, 2), nullable=False)
    purchase_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
