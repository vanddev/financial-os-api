from fastapi import APIRouter

from app.shared.responses.api import SuccessResponse
from app.modules.dashboard.router import get_dashboard_summary
from app.core.database import SessionLocal

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get("/", response_model=SuccessResponse)
def list_kpis():
    """Backward-compatible mapping: /kpis -> /dashboard/summary
    Open a DB session and call dashboard.get_dashboard_summary with it."""
    db = SessionLocal()
    try:
        return get_dashboard_summary(db=db)
    finally:
        db.close()

