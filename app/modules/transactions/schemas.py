from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.modules.transactions.source_rules import validate_transaction_source
from app.shared.domain_enums import CashFlowType, PaymentMethod, TransactionStatus


class TransactionBase(BaseModel):
    account_id: int | None = Field(
        default=None,
        description=(
            "Required only for debit_card, pix, bank_transfer and "
            "automatic_debit payment methods."
        ),
    )
    category_id: int
    subcategory_id: int | None = None
    credit_card_id: int | None = Field(
        default=None,
        description="Required only when payment_method is credit_card.",
    )
    description: str | None = None
    amount: Decimal = Field(gt=0)
    transaction_type: CashFlowType
    payment_method: PaymentMethod | None = None
    status: TransactionStatus | None = None
    transaction_date: datetime
    competency_date: datetime | None = None
    installment_number: int | None = None
    installment_total: int | None = None
    notes: str | None = None
    tags: dict | list | None = None

    @model_validator(mode="after")
    def installment_consistency(self) -> "TransactionBase":
        if self.installment_number is not None and self.installment_total is None:
            raise ValueError("installment_total must be provided when installment_number is set")
        validate_transaction_source(
            payment_method=self.payment_method,
            account_id=self.account_id,
            credit_card_id=self.credit_card_id,
        )
        return self


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    subcategory_id: int | None = None
    credit_card_id: int | None = None
    description: str | None = None
    amount: Decimal | None = Field(default=None, gt=0)
    transaction_type: CashFlowType | None = None
    payment_method: PaymentMethod | None = None
    status: TransactionStatus | None = None
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
