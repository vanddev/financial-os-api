from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.shared.domain_enums import LoanType


class LoanBase(BaseModel):
    name: str
    loan_type: LoanType | None = None
    original_amount: Decimal
    current_balance: Decimal
    interest_rate: Decimal | None = None
    total_installments: int | None = None
    paid_installments: int | None = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    name: str | None = None
    loan_type: LoanType | None = None
    original_amount: Decimal | None = None
    current_balance: Decimal | None = None
    interest_rate: Decimal | None = None
    total_installments: int | None = None
    paid_installments: int | None = None


class LoanOut(LoanBase):
    id: int
    original_amount: float
    current_balance: float
    interest_rate: float | None = None
    remaining_installments: int | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class LoanListResponse(BaseModel):
    items: list[LoanOut]
    page: int
    page_size: int
    total: int


class LoanAmortizationItem(BaseModel):
    month: str
    interest: float
    principal: float
    balance: float
