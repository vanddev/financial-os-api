from datetime import date
from typing import Literal

from pydantic import BaseModel


class OverviewResponse(BaseModel):
    month: int
    year: int
    income: float
    expenses: float
    net_flow: float
    savings: float
    scheduled_commitments: float
    budget_planned: float
    budget_remaining: float
    net_worth: float


class TimeSeriesItem(BaseModel):
    period: str
    income: float
    expenses: float
    net_flow: float


class CategoryExpense(BaseModel):
    category_id: int
    category_name: str
    amount: float


class CashFlowResponse(BaseModel):
    start_date: date
    end_date: date
    income: float
    expenses: float
    net_flow: float
    series: list[TimeSeriesItem]
    expenses_by_category: list[CategoryExpense]


class BudgetCategoryStatus(BaseModel):
    category_id: int
    category_name: str
    planned: float
    actual: float
    remaining: float
    percentage_used: float | None
    status: Literal["within_budget", "exceeded", "unbudgeted"]


class BudgetStatusResponse(BaseModel):
    month: int
    year: int
    planned: float
    actual: float
    remaining: float
    categories: list[BudgetCategoryStatus]


class CreditCardExpense(BaseModel):
    transaction_id: int
    description: str | None
    amount: float
    transaction_date: date


class CreditCardStatus(BaseModel):
    id: int
    name: str
    active: bool
    limit: float
    cycle_start: date
    cycle_end: date
    cycle_spending: float
    available_limit: float
    utilization_percentage: float
    largest_expenses: list[CreditCardExpense]


class CreditCardsResponse(BaseModel):
    reference_date: date
    cards: list[CreditCardStatus]


class InvestmentPosition(BaseModel):
    id: int
    ticker: str
    asset_type: str | None
    quantity: float
    cost: float
    current_value: float
    gain_loss: float
    allocation_percentage: float


class AssetPosition(BaseModel):
    id: int
    name: str
    asset_type: str | None
    purchase_value: float
    current_value: float
    gain_loss: float


class PortfolioResponse(BaseModel):
    investment_cost: float
    investment_value: float
    investment_gain_loss: float
    investments: list[InvestmentPosition]
    other_assets_value: float
    other_assets: list[AssetPosition]
    account_balance: float
    debt_balance: float
    net_worth: float
