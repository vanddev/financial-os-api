from fastapi import APIRouter

from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get("/", response_model=SuccessResponse)
def list_kpis():
    return {"success": True, "data": {"items": [], "page": 1, "page_size": 20, "total": 0}}
