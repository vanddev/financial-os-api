import json
from decimal import Decimal

import pytest

from app.modules.accounts.dto import AccountDTO
from app.modules.assets.schemas import AssetOut
from app.modules.budgets.schemas import BudgetOut
from app.modules.credit_cards.dto import CreditCardDTO
from app.modules.goals.dto import GoalDTO
from app.modules.investments.schemas import InvestmentOut
from app.modules.loans.schemas import LoanOut
from app.modules.settings.schemas import SettingsOut
from app.modules.subscriptions.dto import SubscriptionDTO
from app.modules.transactions.dto import TransactionDTO


@pytest.mark.parametrize(
    ("model", "field", "value"),
    [
        (AccountDTO, "current_balance", Decimal("123.45")),
        (CreditCardDTO, "limit", Decimal("5000.00")),
        (GoalDTO, "target_amount", Decimal("1000.00")),
        (SubscriptionDTO, "monthly_value", Decimal("39.90")),
        (TransactionDTO, "amount", Decimal("12.34")),
        (AssetOut, "current_value", Decimal("250.00")),
        (BudgetOut, "planned_amount", Decimal("800.00")),
        (InvestmentOut, "current_price", Decimal("42.50")),
        (LoanOut, "current_balance", Decimal("900.00")),
        (SettingsOut, "emergency_fund_target", Decimal("45000.00")),
    ],
)
def test_monetary_response_fields_are_json_numbers(model, field, value):
    assert "Decimal" not in str(model.model_fields[field].annotation)

    serialized = json.loads(model.model_construct(**{field: value}).model_dump_json())

    assert isinstance(serialized[field], (int, float))
    assert not isinstance(serialized[field], str)
