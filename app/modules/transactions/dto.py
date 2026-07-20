from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator


class TransactionDTO(BaseModel):
    id: int
    account_id: int | None = None
    category_id: int | None = None
    subcategory_id: int | None = None
    credit_card_id: int | None = None
    description: str | None = None
    amount: float
    transaction_type: str | None = None
    payment_method: str | None = None
    status: str | None = None
    transaction_date: datetime
    competency_date: datetime | None = None
    installment_number: int | None = None
    installment_total: int | None = None
    notes: str | None = None
    tags: list[str] | dict | None = None
    created_at: datetime
    updated_at: datetime

    # Computed fields matching frontend data structure
    account: str | None = None
    category: str | None = None
    subcategory: str | None = None
    card: str | None = None
    installments: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def populate_names(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return data

        # Get values from ORM object relationships
        account_name = None
        if hasattr(data, "account") and data.account:
            account_name = data.account.name

        category_name = None
        if hasattr(data, "category") and data.category:
            category_name = data.category.name

        subcategory_name = None
        if hasattr(data, "subcategory") and data.subcategory:
            subcategory_name = data.subcategory.name

        card_name = None
        if hasattr(data, "credit_card") and data.credit_card:
            card_name = data.credit_card.name

        inst_str = None
        if getattr(data, "installment_number", None) and getattr(data, "installment_total", None):
            inst_str = f"{data.installment_number}/{data.installment_total}"

        # Build a dict representing the dto fields
        result = {
            "id": getattr(data, "id", None),
            "account_id": getattr(data, "account_id", None),
            "category_id": getattr(data, "category_id", None),
            "subcategory_id": getattr(data, "subcategory_id", None),
            "credit_card_id": getattr(data, "credit_card_id", None),
            "description": getattr(data, "description", None),
            "amount": getattr(data, "amount", None),
            "transaction_type": getattr(data, "transaction_type", None),
            "payment_method": getattr(data, "payment_method", None),
            "status": getattr(data, "status", None),
            "transaction_date": getattr(data, "transaction_date", None),
            "competency_date": getattr(data, "competency_date", None),
            "installment_number": getattr(data, "installment_number", None),
            "installment_total": getattr(data, "installment_total", None),
            "notes": getattr(data, "notes", None),
            "tags": getattr(data, "tags", None),
            "created_at": getattr(data, "created_at", None),
            "updated_at": getattr(data, "updated_at", None),
            "account": account_name,
            "category": category_name,
            "subcategory": subcategory_name,
            "card": card_name,
            "installments": inst_str,
        }
        return result
