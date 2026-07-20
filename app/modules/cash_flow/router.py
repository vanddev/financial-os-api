from typing import List
from fastapi import APIRouter

from app.shared.responses.api import SuccessResponse
from app.modules.dashboard.router import get_dashboard_monthly_flow, get_dashboard_cashflow_trend
from app.modules.dashboard.schemas import DashboardCashflowTrendItem, DashboardMonthlyFlowItem
from app.core.database import SessionLocal

router = APIRouter(prefix="/cash_flow", tags=["cash_flow"])


@router.get("/monthly", response_model=SuccessResponse[list[DashboardMonthlyFlowItem]])
def monthly_flow():
    """Legacy endpoint mapping to /dashboard/monthly-flow"""
    db = SessionLocal()
    try:
        return get_dashboard_monthly_flow(db=db)
    finally:
        db.close()


@router.get("/trend", response_model=SuccessResponse[list[DashboardCashflowTrendItem]])
def cashflow_trend():
    """Legacy endpoint mapping to /dashboard/cashflow-trend"""
    db = SessionLocal()
    try:
        return get_dashboard_cashflow_trend(db=db)
    finally:
        db.close()
