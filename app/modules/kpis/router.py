from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.dashboard.router import get_dashboard_summary
from app.modules.dashboard.schemas import DashboardSummary
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get("/", response_model=SuccessResponse[DashboardSummary])
def list_kpis(db: Session = Depends(get_db)):
    """Backward-compatible mapping: /kpis -> /dashboard/summary
    Open a DB session and call dashboard.get_dashboard_summary with it."""
    return get_dashboard_summary(db=db)
