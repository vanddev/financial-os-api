from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.accounts.models import Account
from app.modules.assets.models import Asset
from app.modules.investments.models import Investment
from app.modules.loans.models import Loan
from app.modules.networth.schemas import NetWorthBreakdown, NetWorthSeriesItem
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/net-worth", tags=["networth"])


@router.get("/series", response_model=SuccessResponse[list[NetWorthSeriesItem]])
def get_net_worth_series():
    data = [
        {"month": "Jan", "value": 612000},
        {"month": "Fev", "value": 624500},
        {"month": "Mar", "value": 631200},
        {"month": "Abr", "value": 648000},
        {"month": "Mai", "value": 661300},
        {"month": "Jun", "value": 674100},
        {"month": "Jul", "value": 687420},
    ]
    return {"success": True, "data": data}


@router.get("/breakdown", response_model=SuccessResponse[NetWorthBreakdown])
def get_net_worth_breakdown(db: Session = Depends(get_db)):
    accounts_total = db.query(func.sum(Account.current_balance)).filter(Account.is_active).scalar() or 0
    investments_total = db.query(func.sum(Investment.quantity * (Investment.current_price or Investment.average_price))).scalar() or 0
    assets_total = db.query(func.sum(Asset.current_value)).scalar() or 0
    liabilities_total = db.query(func.sum(Loan.current_balance)).scalar() or 0

    net_worth = assets_total + investments_total + accounts_total - liabilities_total

    return {
        "success": True,
        "data": {
            "accounts_total": float(accounts_total),
            "investments_total": float(investments_total),
            "assets_total": float(assets_total),
            "liabilities_total": float(liabilities_total),
            "net_worth": float(net_worth)
        }
    }
