from datetime import date, datetime
from decimal import Decimal

from app.modules.accounts.models import Account
from app.modules.categories.models import Category
from app.modules.dashboard import services
from app.modules.transactions.models import Transaction


def _freeze_dashboard_date(monkeypatch) -> None:
    monkeypatch.setattr(services, "current_date", lambda: date(2026, 7, 15))


def test_empty_dashboard_does_not_return_mock_financial_data(db_session, monkeypatch) -> None:
    _freeze_dashboard_date(monkeypatch)

    summary = services.get_summary(db_session)

    assert summary.monthly_income == 0
    assert summary.credit_card_debt == 0
    assert summary.emergency_fund == 0
    assert services.get_expense_breakdown(db_session) == []
    assert services.get_cashflow_calendar(db_session) == []


def test_dashboard_reuses_real_cash_flow_data(db_session, monkeypatch) -> None:
    _freeze_dashboard_date(monkeypatch)
    account = Account(
        name="Conta Dashboard",
        type="checking",
        current_balance=Decimal("1000"),
        initial_balance=Decimal("800"),
        is_active=True,
    )
    category = Category(name="Dashboard Food", type="expense")
    db_session.add_all([account, category])
    db_session.commit()
    db_session.add_all(
        [
            Transaction(
                account_id=account.id,
                category_id=category.id,
                amount=Decimal("100"),
                transaction_type="income",
                transaction_date=datetime(2026, 7, 14),
                status="cleared",
                description="Receita real",
            ),
            Transaction(
                account_id=account.id,
                category_id=category.id,
                amount=Decimal("25"),
                transaction_type="expense",
                transaction_date=datetime(2026, 7, 15),
                status="cleared",
                description="Despesa real",
            ),
        ]
    )
    db_session.commit()

    summary = services.get_summary(db_session)
    monthly_flow = services.get_monthly_flow(db_session)
    breakdown = services.get_expense_breakdown(db_session)
    calendar = services.get_cashflow_calendar(db_session)
    trend = services.get_cashflow_trend(db_session)

    assert summary.monthly_income == 100
    assert summary.monthly_expenses == 25
    assert summary.cash_flow_30d == 75
    assert monthly_flow[-1].month == "Jul"
    assert monthly_flow[-1].income == 100
    assert monthly_flow[-1].expenses == 25
    assert breakdown[0].name == "Dashboard Food"
    assert breakdown[0].value == 25
    assert [item.label for item in calendar] == ["Receita real", "Despesa real"]
    assert len(trend) == 30
    assert trend[-1].balance == 1000


def test_cashflow_trend_returns_thirty_days(db_session, monkeypatch) -> None:
    _freeze_dashboard_date(monkeypatch)
    data = services.get_cashflow_trend(db_session)

    assert len(data) == 30
    assert data[0].day == 1
    assert data[-1].day == 30
