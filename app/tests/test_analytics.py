# mypy: disable-error-code="arg-type"

from datetime import date, datetime
from decimal import Decimal

import httpx
import pytest
from fastapi import FastAPI

from app.core.database import get_db
from app.modules.accounts.models import Account
from app.modules.analytics import router, services
from app.modules.assets.models import Asset
from app.modules.budgets.models import Budget
from app.modules.categories.models import Category
from app.modules.credit_cards.models import CreditCard
from app.modules.investments.models import Investment
from app.modules.loans.models import Loan
from app.modules.transactions.models import Transaction


def add_transaction(
    db_session,
    account_id: int,
    category_id: int,
    amount: str,
    transaction_type: str,
    transaction_date: datetime,
    *,
    status: str = "cleared",
    credit_card_id: int | None = None,
) -> Transaction:
    transaction = Transaction(
        account_id=account_id,
        category_id=category_id,
        amount=Decimal(amount),
        transaction_type=transaction_type,
        transaction_date=transaction_date,
        status=status,
        credit_card_id=credit_card_id,
        description="Test",
    )
    db_session.add(transaction)
    db_session.commit()
    return transaction


def test_overview_boundaries_statuses_and_normalized_amounts(db_session):
    account = Account(name="Conta", type="checking", current_balance=Decimal("1000"))
    category = Category(name="Casa", type="expense")
    db_session.add_all([account, category])
    db_session.commit()
    add_transaction(db_session, account.id, category.id, "-100", "expense", datetime(2026, 2, 1))
    add_transaction(db_session, account.id, category.id, "500", "income", datetime(2026, 2, 28, 23))
    add_transaction(
        db_session,
        account.id,
        category.id,
        "-40",
        "expense",
        datetime(2026, 2, 10),
        status="scheduled",
    )
    add_transaction(db_session, account.id, category.id, "-900", "expense", datetime(2026, 3, 1))
    db_session.add(Budget(category_id=category.id, month=2, year=2026, planned_amount=300))
    db_session.commit()

    result = services.get_overview(db_session, 2, 2026)

    assert result.income == 500
    assert result.expenses == 100
    assert result.net_flow == 400
    assert result.scheduled_commitments == 40
    assert result.budget_remaining == 200


def test_budget_status_includes_exceeded_and_unbudgeted(db_session):
    account = Account(name="Conta B", type="checking", current_balance=0)
    food = Category(name="Food", type="expense")
    travel = Category(name="Travel", type="expense")
    db_session.add_all([account, food, travel])
    db_session.commit()
    db_session.add(Budget(category_id=food.id, month=7, year=2026, planned_amount=100))
    db_session.commit()
    add_transaction(db_session, account.id, food.id, "-130", "expense", datetime(2026, 7, 2))
    add_transaction(db_session, account.id, travel.id, "50", "expense", datetime(2026, 7, 3))

    result = services.get_budget_status(db_session, 7, 2026)
    states = {item.category_name: item.status for item in result.categories}

    assert states == {"Food": "exceeded", "Travel": "unbudgeted"}
    assert result.actual == 180


def test_credit_card_cycle_handles_february_and_end_of_month(db_session):
    account = Account(name="Conta C", type="checking", current_balance=0)
    category = Category(name="Card", type="expense")
    card = CreditCard(name="Card", limit=1000, closing_day=31, due_day=10, active=True)
    db_session.add_all([account, category, card])
    db_session.commit()
    add_transaction(
        db_session,
        account.id,
        category.id,
        "-100",
        "expense",
        datetime(2026, 2, 28),
        credit_card_id=card.id,
    )

    result = services.get_credit_cards(db_session, date(2026, 2, 15), True)

    assert result.cards[0].cycle_start == date(2026, 2, 1)
    assert result.cards[0].cycle_end == date(2026, 3, 1)
    assert result.cards[0].cycle_spending == 100


def test_empty_database_returns_zeroes(db_session):
    overview = services.get_overview(db_session, 1, 2026)
    portfolio = services.get_portfolio(db_session)

    assert overview.income == overview.expenses == overview.net_worth == 0
    assert portfolio.investments == []
    assert portfolio.other_assets == []


def test_portfolio_current_position(db_session):
    db_session.add_all(
        [
            Account(name="Conta D", type="checking", current_balance=1000),
            Investment(ticker="TEST", quantity=2, average_price=100, current_price=120),
            Asset(name="Car", purchase_value=10000, current_value=9000),
            Loan(name="Loan", original_amount=1000, current_balance=500),
        ]
    )
    db_session.commit()

    result = services.get_portfolio(db_session)

    assert result.investment_cost == 200
    assert result.investment_value == 240
    assert result.investment_gain_loss == 40
    assert result.net_worth == 9740


@pytest.mark.asyncio
async def test_analytics_http_openapi_and_date_validation(db_session):
    app = FastAPI()
    app.include_router(router)

    async def override_db():
        return db_session

    app.dependency_overrides[get_db] = override_db
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/analytics/cash-flow",
            params={"start_date": "2026-07-02", "end_date": "2026-07-01"},
        )
        openapi = await client.get("/openapi.json")

    assert response.status_code == 422
    assert "/analytics/overview" in openapi.json()["paths"]
    schema = openapi.json()["paths"]["/analytics/portfolio"]["get"]["responses"]["200"]
    assert "content" in schema
