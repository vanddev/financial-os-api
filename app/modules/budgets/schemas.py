from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BudgetBase(BaseModel):
    category_id: int
    month: int = Field(ge=1, le=12)
    year: int
    planned_amount: Decimal


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category_id: int | None = None
    month: int | None = Field(None, ge=1, le=12)
    year: int | None = None
    planned_amount: Decimal | None = None


class BudgetOut(BudgetBase):
    id: int
    planned_amount: float
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
