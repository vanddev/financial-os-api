from fastapi import APIRouter

from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=SuccessResponse)
def get_settings():
    return {"success": True, "data": {}}
