from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain_enums import AssetType
from app.shared.pagination.paginator import PageResponse


class AssetBase(BaseModel):
    name: str
    asset_type: AssetType | None = None
    purchase_value: Decimal
    current_value: Decimal
    purchase_date: datetime | None = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: str | None = None
    asset_type: AssetType | None = None
    purchase_value: Decimal | None = None
    current_value: Decimal | None = None
    purchase_date: datetime | None = None


class AssetOut(AssetBase):
    id: int
    purchase_value: float
    current_value: float
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AssetListItem(BaseModel):
    id: int
    name: str
    type: AssetType | None = None
    purchase: float
    current: float
    delta: float
    delta_pct: float = Field(alias="deltaPct")
    contributions: float
    purchase_date: str | None = None


class AssetListResponse(PageResponse[AssetListItem]):
    pass
