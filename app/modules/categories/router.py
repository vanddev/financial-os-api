from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.categories.dto import CategoryDTO
from app.shared.pagination.paginator import PageResponse
from app.shared.responses.api import SuccessResponse
from app.modules.categories import service, schemas, models

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=SuccessResponse[PageResponse[CategoryDTO]])
def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    svc = service.CategoryService(db)
    items, total = svc.list(page=page, page_size=page_size, sort=sort, order=order)
    return {
        "success": True,
        "data": {"items": items, "page": page, "page_size": page_size, "total": total},
    }


@router.post("/", response_model=SuccessResponse)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    svc = service.CategoryService(db)
    c = svc.create(payload)
    return {"success": True, "data": c}


@router.get("/{category_id}", response_model=SuccessResponse[CategoryDTO])
def get_category(category_id: int, db: Session = Depends(get_db)):
    svc = service.CategoryService(db)
    c = svc.get(category_id)
    return {"success": True, "data": c}


@router.put("/{category_id}", response_model=SuccessResponse)
def update_category(
    category_id: int, payload: schemas.CategoryUpdate, db: Session = Depends(get_db)
):
    svc = service.CategoryService(db)
    c = svc.update(category_id, payload)
    return {"success": True, "data": c}


@router.delete("/{category_id}", response_model=SuccessResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    svc = service.CategoryService(db)
    svc.delete(category_id)
    return {"success": True, "data": {}}


@router.post("/{category_id}/subcategories", response_model=SuccessResponse)
def create_subcategory(
    category_id: int, payload: schemas.SubcategoryCreate, db: Session = Depends(get_db)
):
    from fastapi import HTTPException

    cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    from app.modules.categories.models import Subcategory

    sub = Subcategory(category_id=category_id, name=payload.name)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return {
        "success": True,
        "data": {"id": sub.id, "category_id": sub.category_id, "name": sub.name},
    }
