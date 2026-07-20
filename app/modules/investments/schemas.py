from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.shared.pagination.paginator import PageResponse


class InvestmentBase(BaseModel):
    ticker: str
    asset_type: str | None = None
    quantity: Decimal
    average_price: Decimal
    current_price: Decimal | None = None
    broker: str | None = None


class InvestmentCreate(InvestmentBase):
    pass


class InvestmentUpdate(BaseModel):
    ticker: str | None = None
    asset_type: str | None = None
    quantity: Decimal | None = None
    average_price: Decimal | None = None
    current_price: Decimal | None = None
    broker: str | None = None


class InvestmentOut(InvestmentBase):
    id: int
    quantity: float
    average_price: float
    current_price: float | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class InvestmentListItem(BaseModel):
    id: int
    ticker: str
    name: str
    type: str | None = None
    qty: float
    avg: float
    price: float
    value: float
    pl: float
    pl_pct: float = Field(alias="plPct")


class InvestmentListResponse(PageResponse[InvestmentListItem]):
    pass


class InvestmentAllocationItem(BaseModel):
    name: str
    value: float
    color: str


class InvestmentSeriesItem(BaseModel):
    month: str
    value: float
