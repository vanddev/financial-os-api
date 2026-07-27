import calendar
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.accounts.models import Account
from app.modules.analytics import services as analytics_services
from app.modules.categories.models import Category
from app.modules.goals.models import Goal
from app.modules.transactions.models import Transaction
from app.shared.domain_enums import CashFlowType

from . import schemas

ZERO = Decimal("0")
MONTH_LABELS = (
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
)


def current_date() -> date:
    return datetime.now(analytics_services.BAHIA).date()


def _shift_month(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 + months
    year, zero_based_month = divmod(month_index, 12)
    return date(year, zero_based_month + 1, 1)


def _active_accounts(db: Session) -> list[Account]:
    return list(db.scalars(select(Account).where(Account.is_active.is_(True))).all())


def get_summary(db: Session) -> schemas.DashboardSummary:
    today = current_date()
    overview = analytics_services.get_overview(db, today.month, today.year)
    portfolio = analytics_services.get_portfolio(db)
    accounts = _active_accounts(db)

    liquid_balance = sum(
        (
            Decimal(str(account.current_balance))
            for account in accounts
            if account.type in {"checking", "savings"}
        ),
        ZERO,
    )
    available_cash = sum(
        (
            Decimal(str(account.current_balance))
            for account in accounts
            if account.type in {"checking", "cash"}
        ),
        ZERO,
    )

    emergency_goal = db.scalar(select(Goal).where(Goal.name.ilike("%emergência%")).limit(1))
    if emergency_goal is None:
        emergency_fund = sum(
            (
                Decimal(str(account.current_balance))
                for account in accounts
                if "emergência" in account.name.casefold()
            ),
            ZERO,
        )
        emergency_target = ZERO
    else:
        emergency_fund = Decimal(str(emergency_goal.current_amount))
        emergency_target = Decimal(str(emergency_goal.target_amount))

    card_status = analytics_services.get_credit_cards(db, today, active=True)
    credit_card_debt = sum((Decimal(str(card.cycle_spending)) for card in card_status.cards), ZERO)
    thirty_day_flow = analytics_services.get_cash_flow(
        db,
        today - timedelta(days=29),
        today + timedelta(days=1),
        "day",
        account_id=None,
    )
    investment_growth = (
        portfolio.investment_gain_loss / portfolio.investment_cost * 100
        if portfolio.investment_cost
        else 0
    )
    savings_rate = overview.net_flow / overview.income * 100 if overview.income else 0

    return schemas.DashboardSummary(
        currentBalance=float(liquid_balance),
        netWorth=portfolio.net_worth,
        monthlyIncome=overview.income,
        monthlyExpenses=overview.expenses,
        savingsRate=round(savings_rate, 1),
        investmentGrowth=round(investment_growth, 1),
        emergencyFund=float(emergency_fund),
        emergencyFundTarget=float(emergency_target),
        creditCardDebt=float(credit_card_debt),
        upcomingBills=overview.scheduled_commitments,
        availableCash=float(available_cash),
        cashFlow30d=thirty_day_flow.net_flow,
    )


def get_monthly_flow(db: Session) -> list[schemas.DashboardMonthlyFlowItem]:
    first_month = _shift_month(current_date().replace(day=1), -6)
    end = _shift_month(first_month, 7)
    cash_flow = analytics_services.get_cash_flow(db, first_month, end, "month", account_id=None)
    totals = {item.period: item for item in cash_flow.series}

    result = []
    for offset in range(7):
        month = _shift_month(first_month, offset)
        item = totals.get(month.strftime("%Y-%m"))
        result.append(
            schemas.DashboardMonthlyFlowItem(
                month=MONTH_LABELS[month.month - 1],
                income=item.income if item else 0,
                expenses=item.expenses if item else 0,
            )
        )
    return result


def get_cashflow_trend(db: Session) -> list[schemas.DashboardCashflowTrendItem]:
    end_date = current_date() + timedelta(days=1)
    start_date = end_date - timedelta(days=30)
    cash_flow = analytics_services.get_cash_flow(db, start_date, end_date, "day", account_id=None)
    daily_net = {item.period: Decimal(str(item.net_flow)) for item in cash_flow.series}
    ending_balance = sum(
        (Decimal(str(account.current_balance)) for account in _active_accounts(db)),
        ZERO,
    )
    balance = ending_balance - Decimal(str(cash_flow.net_flow))

    result = []
    for offset in range(30):
        selected_date = start_date + timedelta(days=offset)
        balance += daily_net.get(selected_date.isoformat(), ZERO)
        result.append(
            schemas.DashboardCashflowTrendItem(
                day=offset + 1,
                balance=float(balance),
            )
        )
    return result


def get_expense_breakdown(
    db: Session,
) -> list[schemas.DashboardExpenseBreakdownItem]:
    today = current_date()
    start_date = today.replace(day=1)
    end_date = _shift_month(start_date, 1)
    cash_flow = analytics_services.get_cash_flow(db, start_date, end_date, "month", account_id=None)
    return [
        schemas.DashboardExpenseBreakdownItem(
            name=item.category_name,
            value=item.amount,
        )
        for item in cash_flow.expenses_by_category
    ]


def get_cashflow_calendar(
    db: Session,
) -> list[schemas.DashboardCashflowCalendarItem]:
    today = current_date()
    start = datetime(today.year, today.month, 1)
    end = datetime(
        today.year,
        today.month,
        calendar.monthrange(today.year, today.month)[1],
        23,
        59,
        59,
        999999,
    )
    transactions = list(
        db.scalars(
            select(Transaction)
            .where(
                Transaction.transaction_date >= start,
                Transaction.transaction_date <= end,
                Transaction.status.in_(("cleared", "scheduled")),
            )
            .order_by(Transaction.transaction_date, Transaction.id)
        ).all()
    )
    category_names: dict[int, str] = {
        cast(int, category.id): cast(str, category.name)
        for category in db.scalars(select(Category)).all()
    }
    return [
        schemas.DashboardCashflowCalendarItem(
            day=transaction.transaction_date.day,
            label=cast(str | None, transaction.description)
            or category_names.get(cast(int, transaction.category_id), "Transação"),
            amount=float(transaction.amount),
            type=CashFlowType(cast(str, transaction.transaction_type)),
        )
        for transaction in transactions
        if transaction.transaction_type in {"income", "expense"}
    ]
