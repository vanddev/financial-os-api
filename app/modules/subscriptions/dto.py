from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubscriptionDTO(BaseModel):
    id: int
    name: str
    category: str | None = None
    monthly_value: float
    yearly_value: float | None = 0.0
    renewal_date: datetime | None = None
    days_until_renewal: int | None = None
    payment_method: str | None = None
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
