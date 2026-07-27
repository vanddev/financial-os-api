# mypy: disable-error-code="arg-type,index,call-overload"

import calendar
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Literal, cast
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.accounts.models import Account
from app.modules.assets.models import Asset
from app.modules.budgets.models import Budget
from app.modules.categories.models import Category, Subcategory
from app.modules.credit_cards.models import CreditCard
from app.modules.investments.models import Investment
from app.modules.loans.models import Loan
from app.modules.transactions.models import Transaction

from . import schemas

BAHIA = ZoneInfo("America/Bahia")
ZERO = Decimal("0")


def current_month_year() -> tuple[int, int]:
    now = datetime.now(BAHIA)
    return now.month, now.year


def month_bounds(month: int, year: int) -> tuple[datetime, datetime]:
    start = datetime(year, month, 1)
    if month == 12:
        return start, datetime(year + 1, 1, 1)
    return start, datetime(year, month + 1, 1)


def _money(value: Decimal | int | None) -> float:
    return float(value or ZERO)


def _positive_amount(transaction: Transaction) -> Decimal:
    return Decimal(transaction.amount)


def _transactions(
    db: Session,
    start: datetime,
    end: datetime,
    *,
    status: str = "cleared",
    account_id: int | None = None,
) -> list[Transaction]:
    statement = select(Transaction).where(
        Transaction.transaction_date >= start,
        Transaction.transaction_date < end,
        Transaction.status == status,
    )
    if account_id is not None:
        statement = statement.where(Transaction.account_id == account_id)
    return list(db.scalars(statement).all())


def get_overview(db: Session, month: int, year: int) -> schemas.OverviewResponse:
    start, end = month_bounds(month, year)
    cleared = _transactions(db, start, end)
    scheduled = _transactions(db, start, end, status="scheduled")
    income = sum((_positive_amount(tx) for tx in cleared if tx.transaction_type == "income"), ZERO)
    expenses = sum(
        (_positive_amount(tx) for tx in cleared if tx.transaction_type == "expense"), ZERO
    )
    commitments = sum(
        (_positive_amount(tx) for tx in scheduled if tx.transaction_type == "expense"), ZERO
    )
    planned = sum(
        (
            Decimal(budget.planned_amount)
            for budget in db.scalars(
                select(Budget).where(Budget.month == month, Budget.year == year)
            )
        ),
        ZERO,
    )
    portfolio = get_portfolio(db)
    net = income - expenses
    return schemas.OverviewResponse(
        month=month,
        year=year,
        income=_money(income),
        expenses=_money(expenses),
        net_flow=_money(net),
        savings=_money(net),
        scheduled_commitments=_money(commitments),
        budget_planned=_money(planned),
        budget_remaining=_money(planned - expenses),
        net_worth=portfolio.net_worth,
    )


def get_cash_flow(
    db: Session,
    start_date: date,
    end_date: date,
    group_by: str,
    account_id: int | None,
) -> schemas.CashFlowResponse:
    start = datetime.combine(start_date, datetime.min.time())
    end = datetime.combine(end_date, datetime.min.time())
    txs = _transactions(db, start, end, account_id=account_id)
    categories = {category.id: category.name for category in db.scalars(select(Category)).all()}
    grouped: dict[str, dict[str, Decimal]] = defaultdict(lambda: {"income": ZERO, "expenses": ZERO})
    category_totals: dict[int, Decimal] = defaultdict(lambda: ZERO)
    for tx in txs:
        key = (
            tx.transaction_date.date().isoformat()
            if group_by == "day"
            else tx.transaction_date.strftime("%Y-%m")
        )
        amount = _positive_amount(tx)
        if tx.transaction_type == "income":
            grouped[key]["income"] += amount
        elif tx.transaction_type == "expense":
            grouped[key]["expenses"] += amount
            category_totals[tx.category_id] += amount
    income = sum((values["income"] for values in grouped.values()), ZERO)
    expenses = sum((values["expenses"] for values in grouped.values()), ZERO)
    return schemas.CashFlowResponse(
        start_date=start_date,
        end_date=end_date,
        income=_money(income),
        expenses=_money(expenses),
        net_flow=_money(income - expenses),
        series=[
            schemas.TimeSeriesItem(
                period=key,
                income=_money(values["income"]),
                expenses=_money(values["expenses"]),
                net_flow=_money(values["income"] - values["expenses"]),
            )
            for key, values in sorted(grouped.items())
        ],
        expenses_by_category=[
            schemas.CategoryExpense(
                category_id=category_id,
                category_name=categories.get(category_id, "Unknown"),
                amount=_money(amount),
            )
            for category_id, amount in sorted(
                category_totals.items(), key=lambda item: item[1], reverse=True
            )
        ],
    )


def get_budget_status(
    db: Session,
    month: int,
    year: int,
    category: int | None = None,
) -> schemas.BudgetStatusResponse:
    start, end = month_bounds(month, year)
    budget_statement = select(Budget).where(Budget.month == month, Budget.year == year)
    selected_category_id: int | None = None
    selected_subcategory_id: int | None = None
    if category is not None:
        selected_category_id = db.scalar(
            select(Category.id).where(Category.id == category)
        )
        if selected_category_id is None:
            subcategory = db.scalar(
                select(Subcategory).where(Subcategory.id == category)
            )
            if subcategory is not None:
                selected_category_id = cast(int, subcategory.category_id)
                selected_subcategory_id = cast(int, subcategory.id)
        if selected_category_id is None:
            budget_statement = budget_statement.where(Budget.category_id == category)
        else:
            budget_statement = budget_statement.where(
                Budget.category_id == selected_category_id
            )
    budgets = list(db.scalars(budget_statement).all())
    names = {category.id: category.name for category in db.scalars(select(Category)).all()}
    planned_by_category: dict[int, Decimal] = defaultdict(lambda: ZERO)
    for budget in budgets:
        planned_by_category[budget.category_id] += Decimal(budget.planned_amount)
    actual_by_category: dict[int, Decimal] = defaultdict(lambda: ZERO)
    for tx in _transactions(db, start, end):
        matches_category = (
            category is None
            or (
                selected_subcategory_id is not None
                and tx.subcategory_id == selected_subcategory_id
            )
            or (
                selected_subcategory_id is None
                and selected_category_id is not None
                and tx.category_id == selected_category_id
            )
        )
        if tx.transaction_type == "expense" and matches_category:
            actual_by_category[tx.category_id] += _positive_amount(tx)
    items = []
    for category_id in sorted(set(planned_by_category) | set(actual_by_category)):
        planned = planned_by_category[category_id]
        actual = actual_by_category[category_id]
        if planned == ZERO:
            state: Literal["within_budget", "exceeded", "unbudgeted"] = "unbudgeted"
            percentage = None
        elif actual > planned:
            state = "exceeded"
            percentage = _money(actual / planned * 100)
        else:
            state = "within_budget"
            percentage = _money(actual / planned * 100)
        items.append(
            schemas.BudgetCategoryStatus(
                category_id=category_id,
                category_name=names.get(category_id, "Unknown"),
                planned=_money(planned),
                actual=_money(actual),
                remaining=_money(planned - actual),
                percentage_used=percentage,
                status=state,
            )
        )
    planned_total = sum(planned_by_category.values(), ZERO)
    actual_total = sum(actual_by_category.values(), ZERO)
    return schemas.BudgetStatusResponse(
        month=month,
        year=year,
        planned=_money(planned_total),
        actual=_money(actual_total),
        remaining=_money(planned_total - actual_total),
        categories=items,
    )


def _safe_date(year: int, month: int, day: int) -> date:
    return date(year, month, min(day, calendar.monthrange(year, month)[1]))


def _shift_month(value: date, months: int) -> tuple[int, int]:
    index = value.year * 12 + value.month - 1 + months
    return divmod(index, 12)[0], divmod(index, 12)[1] + 1


def card_cycle(reference: date, closing_day: int) -> tuple[date, date]:
    closing = _safe_date(reference.year, reference.month, closing_day)
    if reference <= closing:
        previous_year, previous_month = _shift_month(reference, -1)
        previous = _safe_date(previous_year, previous_month, closing_day)
        return previous + timedelta(days=1), closing + timedelta(days=1)
    next_year, next_month = _shift_month(reference, 1)
    next_closing = _safe_date(next_year, next_month, closing_day)
    return closing + timedelta(days=1), next_closing + timedelta(days=1)


def get_credit_cards(
    db: Session, reference_date: date, active: bool | None
) -> schemas.CreditCardsResponse:
    statement = select(CreditCard).order_by(CreditCard.id)
    if active is not None:
        statement = statement.where(CreditCard.active == active)
    cards = []
    for card in db.scalars(statement).all():
        cycle_start, cycle_end = card_cycle(reference_date, card.closing_day or 1)
        txs = list(
            db.scalars(
                select(Transaction).where(
                    Transaction.credit_card_id == card.id,
                    Transaction.transaction_date
                    >= datetime.combine(cycle_start, datetime.min.time()),
                    Transaction.transaction_date < datetime.combine(cycle_end, datetime.min.time()),
                    Transaction.status == "cleared",
                    Transaction.transaction_type == "expense",
                )
            ).all()
        )
        spending = sum((_positive_amount(tx) for tx in txs), ZERO)
        limit = Decimal(card.limit)
        cards.append(
            schemas.CreditCardStatus(
                id=card.id,
                name=card.name,
                active=bool(card.active),
                limit=_money(limit),
                cycle_start=cycle_start,
                cycle_end=cycle_end,
                cycle_spending=_money(spending),
                available_limit=_money(limit - spending),
                utilization_percentage=_money(spending / limit * 100) if limit else 0,
                largest_expenses=[
                    schemas.CreditCardExpense(
                        transaction_id=tx.id,
                        description=tx.description,
                        amount=_money(_positive_amount(tx)),
                        transaction_date=tx.transaction_date.date(),
                    )
                    for tx in sorted(txs, key=_positive_amount, reverse=True)[:5]
                ],
            )
        )
    return schemas.CreditCardsResponse(reference_date=reference_date, cards=cards)


def get_portfolio(db: Session) -> schemas.PortfolioResponse:
    investments = list(db.scalars(select(Investment).order_by(Investment.id)).all())
    values = [
        Decimal(item.quantity) * Decimal(item.current_price or item.average_price)
        for item in investments
    ]
    investment_total = sum(values, ZERO)
    investment_cost = sum(
        (Decimal(item.quantity) * Decimal(item.average_price) for item in investments), ZERO
    )
    positions = [
        schemas.InvestmentPosition(
            id=item.id,
            ticker=item.ticker,
            asset_type=item.asset_type,
            quantity=_money(Decimal(item.quantity)),
            cost=_money(Decimal(item.quantity) * Decimal(item.average_price)),
            current_value=_money(value),
            gain_loss=_money(value - Decimal(item.quantity) * Decimal(item.average_price)),
            allocation_percentage=_money(value / investment_total * 100) if investment_total else 0,
        )
        for item, value in zip(investments, values, strict=True)
    ]
    assets = list(db.scalars(select(Asset).order_by(Asset.id)).all())
    asset_positions = [
        schemas.AssetPosition(
            id=item.id,
            name=item.name,
            asset_type=item.asset_type,
            purchase_value=_money(Decimal(item.purchase_value)),
            current_value=_money(Decimal(item.current_value)),
            gain_loss=_money(Decimal(item.current_value) - Decimal(item.purchase_value)),
        )
        for item in assets
    ]
    assets_total = sum((Decimal(item.current_value) for item in assets), ZERO)
    accounts_total = sum(
        (Decimal(item.current_balance) for item in db.scalars(select(Account))), ZERO
    )
    debt_total = sum((Decimal(item.current_balance) for item in db.scalars(select(Loan))), ZERO)
    return schemas.PortfolioResponse(
        investment_cost=_money(investment_cost),
        investment_value=_money(investment_total),
        investment_gain_loss=_money(investment_total - investment_cost),
        investments=positions,
        other_assets_value=_money(assets_total),
        other_assets=asset_positions,
        account_balance=_money(accounts_total),
        debt_balance=_money(debt_total),
        net_worth=_money(accounts_total + assets_total + investment_total - debt_total),
    )
