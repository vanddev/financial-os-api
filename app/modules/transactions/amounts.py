from decimal import Decimal

from app.shared.domain_enums import CashFlowType


def signed_amount(
    amount: Decimal,
    transaction_type: CashFlowType | str,
) -> Decimal:
    """Return a transaction magnitude with its cash-flow direction applied."""
    if transaction_type == CashFlowType.EXPENSE:
        return -amount
    return amount
