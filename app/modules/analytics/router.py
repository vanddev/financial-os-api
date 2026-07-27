from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.responses.api import SuccessResponse

from . import schemas, services

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _month_year(month: int | None, year: int | None) -> tuple[int, int]:
    current_month, current_year = services.current_month_year()
    return month or current_month, year or current_year


@router.get("/overview", response_model=SuccessResponse[schemas.OverviewResponse])
async def overview(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    selected_month, selected_year = _month_year(month, year)
    return {
        "success": True,
        "data": services.get_overview(db, selected_month, selected_year),
    }


@router.get("/cash-flow", response_model=SuccessResponse[schemas.CashFlowResponse])
async def cash_flow(
    start_date: date,
    end_date: date,
    group_by: Literal["day", "month"] = "day",
    account_id: int | None = None,
    db: Session = Depends(get_db),
):
    if start_date >= end_date:
        raise HTTPException(status_code=422, detail="end_date must be after start_date")
    return {
        "success": True,
        "data": services.get_cash_flow(db, start_date, end_date, group_by, account_id),
    }


@router.get("/budget-status", response_model=SuccessResponse[schemas.BudgetStatusResponse])
async def budget_status(
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    selected_month, selected_year = _month_year(month, year)
    return {
        "success": True,
        "data": services.get_budget_status(db, selected_month, selected_year),
    }


@router.get("/credit-cards", response_model=SuccessResponse[schemas.CreditCardsResponse])
async def credit_cards(
    reference_date: date | None = None,
    active: bool | None = None,
    db: Session = Depends(get_db),
):
    selected_date = reference_date or datetime_now_bahia()
    return {
        "success": True,
        "data": services.get_credit_cards(db, selected_date, active),
    }


def datetime_now_bahia() -> date:
    from datetime import datetime

    return datetime.now(services.BAHIA).date()


@router.get("/portfolio", response_model=SuccessResponse[schemas.PortfolioResponse])
async def portfolio(db: Session = Depends(get_db)):
    return {"success": True, "data": services.get_portfolio(db)}
