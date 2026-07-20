from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GoalDTO(BaseModel):
    id: int
    name: str
    target_amount: float
    current_amount: float
    deadline: datetime | None = None
    color: str | None = None
    completed: bool
    pct_complete: float | None = 0.0
    eta: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
