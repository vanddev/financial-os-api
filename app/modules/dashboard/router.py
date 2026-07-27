from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.dashboard import services
from app.modules.dashboard.schemas import (
    DashboardCashflowCalendarItem,
    DashboardCashflowTrendItem,
    DashboardExpenseBreakdownItem,
    DashboardMonthlyFlowItem,
    DashboardSummary,
)
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=SuccessResponse[DashboardSummary])
def get_dashboard_summary(db: Session = Depends(get_db)):
    return {"success": True, "data": services.get_summary(db)}


@router.get("/monthly-flow", response_model=SuccessResponse[list[DashboardMonthlyFlowItem]])
def get_dashboard_monthly_flow(db: Session = Depends(get_db)):
    return {"success": True, "data": services.get_monthly_flow(db)}


@router.get("/cashflow-trend", response_model=SuccessResponse[list[DashboardCashflowTrendItem]])
def get_dashboard_cashflow_trend(db: Session = Depends(get_db)):
    return {"success": True, "data": services.get_cashflow_trend(db)}


@router.get(
    "/expense-breakdown", response_model=SuccessResponse[list[DashboardExpenseBreakdownItem]]
)
def get_dashboard_expense_breakdown(db: Session = Depends(get_db)):
    return {"success": True, "data": services.get_expense_breakdown(db)}


@router.get(
    "/cashflow-calendar", response_model=SuccessResponse[list[DashboardCashflowCalendarItem]]
)
def get_dashboard_cashflow_calendar(db: Session = Depends(get_db)):
    return {"success": True, "data": services.get_cashflow_calendar(db)}
