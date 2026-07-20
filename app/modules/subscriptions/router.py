from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.responses.api import SuccessResponse
from app.modules.subscriptions.models import Subscription
from app.modules.subscriptions.schemas import SubscriptionCreate, SubscriptionUpdate
from app.modules.subscriptions.dto import SubscriptionDTO
from app.shared.pagination.paginator import PageResponse

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/", response_model=SuccessResponse[PageResponse[SubscriptionDTO]])
def list_subscriptions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    active: bool | None = None,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    query = db.query(Subscription)
    if active is not None:
        query = query.filter(Subscription.active == active)
        
    total = query.count()
    items = query.offset(offset).limit(page_size).all()
    
    today = datetime.utcnow()
    enriched_items = []
    for item in items:
        # Compute computed fields
        item.yearly_value = item.monthly_value * 12
        
        days = None
        if item.renewal_date is not None:
            delta = item.renewal_date - today
            days = max(0, delta.days)
            
        item.days_until_renewal = days
        enriched_items.append(item)
        
    return {"success": True, "data": {"items": enriched_items, "page": page, "page_size": page_size, "total": total}}


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db)):
    sub = Subscription(
        name=payload.name,
        category=payload.category,
        monthly_value=payload.monthly_value,
        renewal_date=payload.renewal_date,
        payment_method=payload.payment_method,
        active=payload.active
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return {"success": True, "data": sub}


@router.get("/{sub_id}", response_model=SuccessResponse[SubscriptionDTO])
def get_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    today = datetime.utcnow()
    sub.yearly_value = sub.monthly_value * 12
    days = None
    if sub.renewal_date is not None:
        delta = sub.renewal_date - today
        days = max(0, delta.days)
    sub.days_until_renewal = days
    
    return {"success": True, "data": sub}


@router.put("/{sub_id}", response_model=SuccessResponse)
def update_subscription(sub_id: int, payload: SubscriptionUpdate, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(sub, k, v)
        
    db.commit()
    db.refresh(sub)
    return {"success": True, "data": sub}


@router.delete("/{sub_id}", response_model=SuccessResponse)
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
        
    db.delete(sub)
    db.commit()
    return {"success": True, "data": {}}
