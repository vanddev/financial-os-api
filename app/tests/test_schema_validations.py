import pytest
from decimal import Decimal
from datetime import datetime

from app.modules.transactions import schemas as tx_schemas


def test_transaction_amount_zero_raises():
    with pytest.raises(ValueError):
        tx_schemas.TransactionCreate(account_id=1, category_id=1, amount=Decimal("0"), transaction_type="expense", transaction_date=datetime.utcnow())
