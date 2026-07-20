from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.accounts.dto import AccountDTO
from app.modules.transactions.dto import TransactionDTO
from app.shared.pagination.paginator import PageResponse
from app.shared.responses.api import SuccessResponse
from app.shared.responses.schemas import HistoricalValue
from app.modules.accounts import service, schemas

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=SuccessResponse[PageResponse[AccountDTO]])
def list_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    active: bool | None = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    svc = service.AccountService(db)
    items, total = svc.list(page=page, page_size=page_size, active=active, sort=sort, order=order)

    from app.modules.transactions.models import Transaction
    from datetime import datetime

    start_date = datetime(2025, 7, 1)
    end_date = datetime(2025, 7, 31, 23, 59, 59)

    enriched_items = []
    for item in items:
        # Sum income
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.account_id == item.id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.status == "cleared"
        ).scalar() or Decimal("0.00")

        # Sum expense
        expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.account_id == item.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.status == "cleared"
        ).scalar() or Decimal("0.00")

        item.income = income
        item.expenses = abs(expenses)
        enriched_items.append(item)

    return {"success": True, "data": {"items": enriched_items, "page": page, "page_size": page_size, "total": total}}


@router.post("/", response_model=SuccessResponse)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db)):
    svc = service.AccountService(db)
    acc = svc.create(payload)
    return {"success": True, "data": acc}


@router.get("/{account_id}/balance-history", response_model=SuccessResponse[list[HistoricalValue]])
def get_account_balance_history(account_id: int, db: Session = Depends(get_db)):
    from app.modules.transactions.models import Transaction
    from collections import defaultdict
    from datetime import datetime

    svc = service.AccountService(db)
    account = svc.get(account_id)

    txs = db.query(Transaction).filter(
        Transaction.account_id == account_id,
        Transaction.status == "cleared"
    ).order_by(Transaction.transaction_date.desc()).all()

    current_val = account.current_balance
    monthly_sums = defaultdict(Decimal)
    for tx in txs:
        date = tx.transaction_date
        monthly_sums[(date.year, date.month)] += tx.amount

    months_keys = [
        (2025, 7), (2025, 6), (2025, 5), (2025, 4), (2025, 3), (2025, 2)
    ]

    balances = {}
    temp_balance = current_val
    for y, m in months_keys:
        balances[(y, m)] = temp_balance
        temp_balance -= monthly_sums[(y, m)]

    month_names = {
        2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun", 7: "Jul"
    }

    result = []
    for y, m in reversed(months_keys):
        result.append({
            "month": month_names[m],
            "value": float(balances.get((y, m), Decimal("0.00")))
        })

    return {"success": True, "data": result}


@router.get("/{account_id}/transactions", response_model=SuccessResponse[PageResponse[TransactionDTO]])
def get_account_transactions(
    account_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    status: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = Depends(get_db)
):
    from app.modules.transactions.service import TransactionService
    from app.modules.transactions.dto import TransactionDTO

    svc = TransactionService(db)
    filters = {
        "account_id": account_id,
        "status": status,
        "start_date": start_date,
        "end_date": end_date,
    }
    items, total = svc.list(page=page, page_size=page_size, filters=filters, sort="transaction_date", order="desc")
    dto_items = [TransactionDTO.model_validate(item) for item in items]
    return {"success": True, "data": {"items": dto_items, "page": page, "page_size": page_size, "total": total}}


@router.get("/{account_id}", response_model=SuccessResponse[AccountDTO])
def get_account(account_id: int, db: Session = Depends(get_db)):
    svc = service.AccountService(db)
    acc = svc.get(account_id)
    return {"success": True, "data": acc}


@router.put("/{account_id}", response_model=SuccessResponse[AccountDTO])
def update_account(account_id: int, payload: schemas.AccountUpdate, db: Session = Depends(get_db)):
    svc = service.AccountService(db)
    acc = svc.update(account_id, payload)
    return {"success": True, "data": acc}


@router.delete("/{account_id}", response_model=SuccessResponse)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    svc = service.AccountService(db)
    svc.delete(account_id)
    return {"success": True, "data": {}}
