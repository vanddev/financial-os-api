from pydantic import BaseModel


class NetWorthSeriesItem(BaseModel):
    month: str
    value: float


class NetWorthBreakdown(BaseModel):
    accounts_total: float
    investments_total: float
    assets_total: float
    liabilities_total: float
    net_worth: float
