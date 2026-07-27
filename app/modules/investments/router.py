from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.investments.models import Investment
from app.modules.investments.schemas import (
    InvestmentAllocationItem,
    InvestmentCreate,
    InvestmentListResponse,
    InvestmentOut,
    InvestmentSeriesItem,
    InvestmentUpdate,
)
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/investments", tags=["investments"])


@router.get("/allocation", response_model=SuccessResponse[list[InvestmentAllocationItem]])
def get_investments_allocation(db: Session = Depends(get_db)):
    investments = db.query(Investment).all()

    # Calculate total value of the portfolio
    totals_by_type = {}
    total_portfolio_value = Decimal("0.00")

    for inv in investments:
        price = inv.current_price or inv.average_price
        val = inv.quantity * price
        asset_type = inv.asset_type or "other"
        totals_by_type[asset_type] = totals_by_type.get(asset_type, Decimal("0.00")) + val
        total_portfolio_value += val

    allocation = []
    if total_portfolio_value > 0:
        for asset_type, val in totals_by_type.items():
            pct = (val / total_portfolio_value) * 100
            allocation.append(
                {
                    "name": asset_type,
                    "value": round(float(pct), 1),
                }
            )
    else:
        # Default mock if empty
        allocation = [
            {"name": "stock", "value": 42},
            {"name": "etf", "value": 24},
            {"name": "treasury_bond", "value": 18},
            {"name": "cryptocurrency", "value": 9},
            {"name": "fund", "value": 7},
        ]

    return {"success": True, "data": allocation}


@router.get("/performance", response_model=SuccessResponse[list[InvestmentSeriesItem]])
def get_investments_performance():
    data = [
        {"month": "Jan", "value": 92000},
        {"month": "Fev", "value": 98400},
        {"month": "Mar", "value": 105300},
        {"month": "Abr", "value": 112800},
        {"month": "Mai", "value": 128900},
        {"month": "Jun", "value": 138200},
        {"month": "Jul", "value": 148320},
    ]
    return {"success": True, "data": data}


@router.get("/dividends", response_model=SuccessResponse[list[InvestmentSeriesItem]])
def get_investments_dividends():
    data = [
        {"month": "Fev", "value": 180},
        {"month": "Mar", "value": 220},
        {"month": "Abr", "value": 190},
        {"month": "Mai", "value": 260},
        {"month": "Jun", "value": 310},
        {"month": "Jul", "value": 340},
    ]
    return {"success": True, "data": data}


@router.get("/", response_model=SuccessResponse[InvestmentListResponse])
def list_investments(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1), db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    query = db.query(Investment)
    total = query.count()
    items = query.offset(offset).limit(page_size).all()

    result = []
    for item in items:
        qty = item.quantity
        avg = item.average_price
        curr = item.current_price or avg

        total_val = qty * curr
        pl = (curr - avg) * qty
        pl_pct = Decimal("0.00")
        if avg > 0:
            pl_pct = ((curr / avg) - 1) * 100

        result.append(
            {
                "id": item.id,
                "ticker": item.ticker,
                "name": item.ticker,  # Using ticker as name for simplicity, or we can look it up
                "type": item.asset_type,
                "qty": float(qty),
                "avg": float(avg),
                "price": float(curr),
                "value": float(total_val),
                "pl": float(pl),
                "plPct": float(pl_pct),
            }
        )

    return {
        "success": True,
        "data": {"items": result, "page": page, "page_size": page_size, "total": total},
    }


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_investment(payload: InvestmentCreate, db: Session = Depends(get_db)):
    inv = Investment(
        ticker=payload.ticker,
        asset_type=payload.asset_type,
        quantity=payload.quantity,
        average_price=payload.average_price,
        current_price=payload.current_price,
        broker=payload.broker,
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return {"success": True, "data": inv}


@router.get("/{investment_id}", response_model=SuccessResponse[InvestmentOut])
def get_investment(investment_id: int, db: Session = Depends(get_db)):
    inv = db.query(Investment).filter(Investment.id == investment_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investment not found")
    return {"success": True, "data": inv}


@router.put("/{investment_id}", response_model=SuccessResponse)
def update_investment(investment_id: int, payload: InvestmentUpdate, db: Session = Depends(get_db)):
    inv = db.query(Investment).filter(Investment.id == investment_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investment not found")

    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(inv, k, v)

    db.commit()
    db.refresh(inv)
    return {"success": True, "data": inv}


@router.delete("/{investment_id}", response_model=SuccessResponse)
def delete_investment(investment_id: int, db: Session = Depends(get_db)):
    inv = db.query(Investment).filter(Investment.id == investment_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investment not found")

    db.delete(inv)
    db.commit()
    return {"success": True, "data": {}}
