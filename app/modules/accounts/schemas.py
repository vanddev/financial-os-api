from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, condecimal, constr

from app.shared.domain_enums import AccountType

PositiveMoney = condecimal(max_digits=12, decimal_places=2)


class AccountBase(BaseModel):
    name: constr(min_length=1, max_length=120)
    institution: str | None = None
    type: AccountType
    is_active: bool = True


class AccountCreate(AccountBase):
    initial_balance: PositiveMoney = Field(0)


class AccountUpdate(AccountBase):
    initial_balance: PositiveMoney | None = None
    current_balance: PositiveMoney | None = None


class AccountOut(AccountBase):
    id: int
    current_balance: float
    initial_balance: float
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
