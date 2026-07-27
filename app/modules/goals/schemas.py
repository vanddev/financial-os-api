from datetime import datetime

from pydantic import BaseModel, condecimal, constr

Money = condecimal(max_digits=14, decimal_places=2)


class GoalBase(BaseModel):
    name: constr(min_length=1, max_length=150)
    target_amount: Money
    current_amount: Money | None = 0
    deadline: datetime | None = None
    completed: bool = False


class GoalCreate(GoalBase):
    pass


class GoalUpdate(GoalBase):
    pass


class GoalOut(GoalBase):
    id: int
    target_amount: float
    current_amount: float
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
