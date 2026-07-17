from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class CreditCardDTO(BaseModel):
    id: int
    name: str
    issuer: str
    last_four: str
    limit: Decimal
    closing_day: Decimal
    due_day: int
    color: str
    active: bool
    created_at: datetime
    updated_at: datetime\

    model_config = ConfigDict(from_attributes=True)
