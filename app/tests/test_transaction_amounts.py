from decimal import Decimal

from app.modules.transactions.amounts import signed_amount
from app.shared.domain_enums import CashFlowType


def test_signed_amount_applies_transaction_direction():
    amount = Decimal("125.50")

    assert signed_amount(amount, CashFlowType.INCOME) == Decimal("125.50")
    assert signed_amount(amount, CashFlowType.EXPENSE) == Decimal("-125.50")
