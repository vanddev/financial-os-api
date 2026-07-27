from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CreditCardBase(BaseModel):
    name: str
    issuer: str | None = None
    last_four: str | None = None
    limit: Decimal = Decimal("0.00")
    closing_day: int | None = None
    due_day: int | None = None
    active: bool = True


class CreditCardCreate(CreditCardBase):
    pass


class CreditCardUpdate(BaseModel):
    name: str | None = None
    issuer: str | None = None
    last_four: str | None = None
    limit: Decimal | None = None
    closing_day: int | None = None
    due_day: int | None = None
    active: bool | None = None


class CreditCardOut(CreditCardBase):
    id: int
    limit: float
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CreditCardInstallmentItem(BaseModel):
    description: str | None = None
    remaining_installments: int
    monthly_value: float
    next_due: str


class CreditCardCategoryBreakdownItem(BaseModel):
    name: str
    value: float


class CreditCardBiggestPurchaseItem(BaseModel):
    description: str | None = None
    amount: float
    date: str
