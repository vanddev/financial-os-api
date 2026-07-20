from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.budgets.models import Budget
from app.modules.budgets.schemas import BudgetCreate, BudgetOut, BudgetUpdate
from app.shared.pagination.paginator import PageResponse
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/", response_model=SuccessResponse[PageResponse[BudgetOut]])
def list_budgets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Budget)
    if month is not None:
        query = query.filter(Budget.month == month)
    if year is not None:
        query = query.filter(Budget.year == year)

    total = query.count()
    items = (
        query.order_by(Budget.year.desc(), Budget.month.desc(), Budget.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "success": True,
        "data": {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    }


@router.post("/", response_model=SuccessResponse[BudgetOut], status_code=status.HTTP_201_CREATED)
def create_budget(payload: BudgetCreate, db: Session = Depends(get_db)):
    budget = Budget(**payload.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return {"success": True, "data": budget}


@router.get("/{budget_id}", response_model=SuccessResponse[BudgetOut])
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return {"success": True, "data": budget}


@router.put("/{budget_id}", response_model=SuccessResponse[BudgetOut])
def update_budget(
    budget_id: int, payload: BudgetUpdate, db: Session = Depends(get_db)
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(budget, field, value)

    db.commit()
    db.refresh(budget)
    return {"success": True, "data": budget}


@router.delete("/{budget_id}", response_model=SuccessResponse[dict[str, bool]])
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if budget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"success": True, "data": {"deleted": True}}
