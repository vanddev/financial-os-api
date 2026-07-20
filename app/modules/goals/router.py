from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.goals.dto import GoalDTO
from app.shared.pagination.paginator import PageResponse
from app.shared.responses.api import SuccessResponse
from app.modules.goals import service, schemas

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/", response_model=SuccessResponse[PageResponse[GoalDTO]])
def list_goals(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1), completed: bool | None = None, sort: str = "id", order: str = "asc", db: Session = Depends(get_db)):
    svc = service.GoalService(db)
    items, total = svc.list(page=page, page_size=page_size, completed=completed, sort=sort, order=order)
    
    from decimal import Decimal
    months_pt = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }
    
    enriched_items = []
    for item in items:
        pct = Decimal("0.00")
        if item.target_amount > 0:
            pct = (item.current_amount / item.target_amount) * 100
        item.pct_complete = pct
        
        eta = None
        if item.deadline is not None:
            eta = f"{months_pt[item.deadline.month]} {item.deadline.year}"
        item.eta = eta
        enriched_items.append(item)
        
    return {"success": True, "data": {"items": enriched_items, "page": page, "page_size": page_size, "total": total}}


@router.post("/", response_model=SuccessResponse)
def create_goal(payload: schemas.GoalCreate, db: Session = Depends(get_db)):
    svc = service.GoalService(db)
    g = svc.create(payload)
    return {"success": True, "data": g}


@router.get("/{goal_id}", response_model=SuccessResponse[GoalDTO])
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    svc = service.GoalService(db)
    g = svc.get(goal_id)
    
    from decimal import Decimal
    months_pt = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }
    
    pct = Decimal("0.00")
    if g.target_amount > 0:
        pct = (g.current_amount / g.target_amount) * 100
    g.pct_complete = pct
    
    eta = None
    if g.deadline is not None:
        eta = f"{months_pt[g.deadline.month]} {g.deadline.year}"
    g.eta = eta
    
    return {"success": True, "data": g}


@router.put("/{goal_id}", response_model=SuccessResponse)
def update_goal(goal_id: int, payload: schemas.GoalUpdate, db: Session = Depends(get_db)):
    svc = service.GoalService(db)
    g = svc.update(goal_id, payload)
    return {"success": True, "data": g}


@router.delete("/{goal_id}", response_model=SuccessResponse)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    svc = service.GoalService(db)
    svc.delete(goal_id)
    return {"success": True, "data": {}}
