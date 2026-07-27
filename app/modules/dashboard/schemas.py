from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain_enums import CashFlowType


class DashboardSummary(BaseModel):
    current_balance: float = Field(alias="currentBalance")
    net_worth: float = Field(alias="netWorth")
    monthly_income: float = Field(alias="monthlyIncome")
    monthly_expenses: float = Field(alias="monthlyExpenses")
    savings_rate: float = Field(alias="savingsRate")
    investment_growth: float = Field(alias="investmentGrowth")
    emergency_fund: float = Field(alias="emergencyFund")
    emergency_fund_target: float = Field(alias="emergencyFundTarget")
    credit_card_debt: float = Field(alias="creditCardDebt")
    upcoming_bills: float = Field(alias="upcomingBills")
    available_cash: float = Field(alias="availableCash")
    cash_flow_30d: float = Field(alias="cashFlow30d")

    model_config = ConfigDict(populate_by_name=True)


class DashboardMonthlyFlowItem(BaseModel):
    month: str
    income: float
    expenses: float


class DashboardCashflowTrendItem(BaseModel):
    day: int
    balance: float


class DashboardExpenseBreakdownItem(BaseModel):
    name: str
    value: float


class DashboardCashflowCalendarItem(BaseModel):
    day: int
    label: str
    amount: float
    type: CashFlowType
