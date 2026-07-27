from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.modules.accounts.schemas import AccountCreate
from app.modules.assets.schemas import AssetCreate
from app.modules.categories.schemas import CategoryCreate
from app.modules.investments.schemas import InvestmentCreate
from app.modules.loans.schemas import LoanCreate
from app.modules.transactions.schemas import TransactionCreate


@pytest.mark.parametrize(
    ("schema", "payload", "field"),
    [
        (
            AccountCreate,
            {
                "name": "Conta",
                "type": "corrente",
                "initial_balance": 0,
            },
            "type",
        ),
        (
            CategoryCreate,
            {"name": "Categoria", "type": "despesa"},
            "type",
        ),
        (
            TransactionCreate,
            {
                "account_id": 1,
                "category_id": 1,
                "amount": -10,
                "transaction_type": "expense",
                "payment_method": "Débito",
                "transaction_date": datetime(2026, 7, 27),
            },
            "payment_method",
        ),
        (
            AssetCreate,
            {
                "name": "Casa",
                "asset_type": "Imóvel",
                "purchase_value": 100,
                "current_value": 100,
            },
            "asset_type",
        ),
        (
            InvestmentCreate,
            {
                "ticker": "TEST3",
                "asset_type": "Ação",
                "quantity": 1,
                "average_price": 10,
            },
            "asset_type",
        ),
        (
            LoanCreate,
            {
                "name": "Financiamento",
                "loan_type": "Imobiliário",
                "original_amount": 100,
                "current_balance": 90,
            },
            "loan_type",
        ),
    ],
)
def test_domain_schemas_reject_noncanonical_values(schema, payload, field):
    with pytest.raises(ValidationError) as exc_info:
        schema.model_validate(payload)

    assert exc_info.value.errors()[0]["loc"] == (field,)


def test_transaction_schema_accepts_canonical_english_values():
    transaction = TransactionCreate(
        account_id=1,
        category_id=1,
        amount=Decimal("-10"),
        transaction_type="expense",
        payment_method="debit_card",
        status="cleared",
        transaction_date=datetime(2026, 7, 27),
    )

    assert transaction.transaction_type.value == "expense"
    assert transaction.payment_method.value == "debit_card"
    assert transaction.status.value == "cleared"


def test_transaction_schema_rejects_removed_brokerage_method():
    with pytest.raises(ValidationError):
        TransactionCreate(
            account_id=1,
            category_id=1,
            amount=Decimal("-10"),
            transaction_type="expense",
            payment_method="brokerage",
            transaction_date=datetime(2026, 7, 27),
        )
