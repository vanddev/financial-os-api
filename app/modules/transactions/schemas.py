from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class TransactionBase(BaseModel):
    account_id: int
    category_id: int
    subcategory_id: int | None = None
    credit_card_id: int | None = None
    description: str | None = None
    amount: Decimal
    transaction_type: str
    payment_method: str | None = None
    status: str | None = None
    transaction_date: datetime
    competency_date: datetime | None = None
    installment_number: int | None = None
    installment_total: int | None = None
    notes: str | None = None
    tags: dict | list | None = None

    @field_validator("amount")
    @classmethod
    def amount_not_zero(cls, v: Decimal) -> Decimal:
        if v == 0:
            raise ValueError("Transaction amount cannot be zero")
        return v

    @model_validator(mode="after")
    def installment_consistency(self) -> "TransactionBase":
        if self.installment_number is not None and self.installment_total is None:
            raise ValueError("installment_total must be provided when installment_number is set")
        return self


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    subcategory_id: int | None = None
    credit_card_id: int | None = None
    description: str | None = None
    amount: Decimal | None = None
    transaction_type: str | None = None
    payment_method: str | None = None
    status: str | None = None
    transaction_date: datetime | None = None
    competency_date: datetime | None = None
    installment_number: int | None = None
    installment_total: int | None = None
    notes: str | None = None
    tags: dict | list | None = None


class TransactionOut(TransactionBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
