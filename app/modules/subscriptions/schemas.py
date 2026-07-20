from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SubscriptionBase(BaseModel):
    name: str
    category: str | None = None
    monthly_value: Decimal
    renewal_date: datetime | None = None
    payment_method: str | None = None
    active: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    monthly_value: Decimal | None = None
    renewal_date: datetime | None = None
    payment_method: str | None = None
    active: bool | None = None


class SubscriptionOut(SubscriptionBase):
    id: int
    monthly_value: float

    model_config = ConfigDict(from_attributes=True)
