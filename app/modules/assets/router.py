from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.shared.responses.api import SuccessResponse
from app.modules.assets.models import Asset
from app.modules.assets.schemas import AssetCreate, AssetListResponse, AssetOut, AssetUpdate

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=SuccessResponse[AssetListResponse])
def list_assets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    query = db.query(Asset)
    total = query.count()
    items = query.offset(offset).limit(page_size).all()
    
    result = []
    for item in items:
        purchase = item.purchase_value
        current = item.current_value
        delta = current - purchase
        delta_pct = Decimal("0.00")
        if purchase > 0:
            delta_pct = (delta / purchase) * 100
            
        result.append({
            "id": item.id,
            "name": item.name,
            "type": item.asset_type,
            "purchase": float(purchase),
            "current": float(current),
            "delta": float(delta),
            "deltaPct": round(float(delta_pct), 1),
            "contributions": float(purchase), # Contributions is purchase value for simplicity
            "purchase_date": item.purchase_date.strftime("%Y-%m-%d") if item.purchase_date else None
        })
        
    return {"success": True, "data": {"items": result, "page": page, "page_size": page_size, "total": total}}


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        name=payload.name,
        asset_type=payload.asset_type,
        purchase_value=payload.purchase_value,
        current_value=payload.current_value,
        purchase_date=payload.purchase_date
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return {"success": True, "data": asset}


@router.get("/{asset_id}", response_model=SuccessResponse[AssetOut])
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"success": True, "data": asset}


@router.put("/{asset_id}", response_model=SuccessResponse)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(asset, k, v)
        
    db.commit()
    db.refresh(asset)
    return {"success": True, "data": asset}


@router.delete("/{asset_id}", response_model=SuccessResponse)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    db.delete(asset)
    db.commit()
    return {"success": True, "data": {}}
