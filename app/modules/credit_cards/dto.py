from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class AccountDTO(BaseModel):
    id: int
    name: str
    institution: str
    type: str
    current_balance: Decimal
    initial_balance: Decimal
    color: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
