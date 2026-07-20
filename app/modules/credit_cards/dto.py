from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreditCardDTO(BaseModel):
    id: int
    name: str
    issuer: str
    last_four: str
    limit: float
    closing_day: int
    due_day: int
    color: str
    active: bool
    current_bill: float | None = 0.0
    available: float | None = 0.0
    utilization: float | None = 0.0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
