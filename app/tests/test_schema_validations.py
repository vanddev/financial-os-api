from datetime import datetime
from decimal import Decimal

import pytest

from app.modules.transactions import schemas as tx_schemas


def test_transaction_create_openapi_has_conditional_sources_as_optional():
    schema = tx_schemas.TransactionCreate.model_json_schema()
    required = set(schema["required"])

    assert required == {
        "category_id",
        "amount",
        "transaction_type",
        "transaction_date",
    }
    assert "account_id" not in required
    assert "credit_card_id" not in required


def test_transaction_amount_zero_raises():
    with pytest.raises(ValueError):
        tx_schemas.TransactionCreate(
            account_id=1,
            category_id=1,
            amount=Decimal("0"),
            transaction_type="expense",
            transaction_date=datetime.utcnow(),
        )


def test_transaction_amount_negative_raises():
    with pytest.raises(ValueError):
        tx_schemas.TransactionCreate(
            account_id=1,
            category_id=1,
            amount=Decimal("-10"),
            transaction_type="expense",
            transaction_date=datetime.utcnow(),
        )


@pytest.mark.parametrize("payment_method", ["debit_card", "pix", "bank_transfer"])
def test_account_payment_methods_require_account_id(payment_method):
    with pytest.raises(ValueError, match="account_id is required"):
        tx_schemas.TransactionCreate(
            category_id=1,
            amount=Decimal("10"),
            transaction_type="expense",
            payment_method=payment_method,
            transaction_date=datetime.utcnow(),
        )


def test_credit_card_payment_requires_credit_card_id():
    with pytest.raises(ValueError, match="credit_card_id is required"):
        tx_schemas.TransactionCreate(
            category_id=1,
            amount=Decimal("10"),
            transaction_type="expense",
            payment_method="credit_card",
            transaction_date=datetime.utcnow(),
        )


def test_credit_card_payment_accepts_card_without_account():
    transaction = tx_schemas.TransactionCreate(
        category_id=1,
        credit_card_id=2,
        amount=Decimal("10"),
        transaction_type="expense",
        payment_method="credit_card",
        transaction_date=datetime.utcnow(),
    )

    assert transaction.account_id is None
    assert transaction.credit_card_id == 2


def test_transaction_rejects_account_and_credit_card_together():
    with pytest.raises(ValueError, match="cannot be provided together"):
        tx_schemas.TransactionCreate(
            account_id=1,
            category_id=1,
            credit_card_id=2,
            amount=Decimal("10"),
            transaction_type="expense",
            payment_method="credit_card",
            transaction_date=datetime.utcnow(),
        )
