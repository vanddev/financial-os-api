from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class GoalDTO(BaseModel):
    id: int
    name: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: datetime
    color: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
