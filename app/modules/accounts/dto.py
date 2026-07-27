from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.shared.domain_enums import AccountType


class AccountDTO(BaseModel):
    id: int
    name: str
    institution: str
    type: AccountType
    current_balance: float
    initial_balance: float
    is_active: bool
    income: float | None = 0.0
    expenses: float | None = 0.0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
