from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.transactions import schemas, service
from app.modules.transactions.dto import TransactionDTO
from app.shared.domain_enums import CashFlowType, TransactionStatus
from app.shared.pagination.paginator import PageResponse
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=SuccessResponse[PageResponse[TransactionDTO]])
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    account_id: int | None = None,
    category_id: int | None = None,
    credit_card_id: int | None = None,
    status: TransactionStatus | None = None,
    transaction_type: CashFlowType | None = None,
    description: str | None = None,
    min_amount: float | None = None,
    max_amount: float | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    sort: str = "id",
    order: str = "desc",
    db: Session = Depends(get_db),
):
    svc = service.TransactionService(db)
    filters = {
        "account_id": account_id,
        "category_id": category_id,
        "credit_card_id": credit_card_id,
        "status": status,
        "transaction_type": transaction_type,
        "description": description,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "start_date": start_date,
        "end_date": end_date,
    }
    items, total = svc.list(page=page, page_size=page_size, filters=filters, sort=sort, order=order)
    return {
        "success": True,
        "data": {"items": items, "page": page, "page_size": page_size, "total": total},
    }


@router.post("/", response_model=SuccessResponse[TransactionDTO])
def create_transaction(
    payload: schemas.TransactionCreate,
    idempotency_key: Annotated[
        str,
        Header(
            alias="Idempotency-Key",
            min_length=1,
            max_length=255,
        ),
    ],
    db: Session = Depends(get_db),
):
    svc = service.TransactionService(db)
    try:
        t = svc.create(payload, idempotency_key=idempotency_key)
    except service.IdempotencyConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Idempotency-Key was already used with a different payload",
        ) from exc
    except service.TransactionSourceError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    return {"success": True, "data": t}


@router.get("/{tx_id}", response_model=SuccessResponse[TransactionDTO])
def get_transaction(tx_id: int, db: Session = Depends(get_db)):
    svc = service.TransactionService(db)
    t = svc.get(tx_id)
    return {"success": True, "data": t}


@router.put("/{tx_id}", response_model=SuccessResponse[TransactionDTO])
def update_transaction(
    tx_id: int, payload: schemas.TransactionUpdate, db: Session = Depends(get_db)
):
    svc = service.TransactionService(db)
    try:
        t = svc.update(tx_id, payload)
    except service.TransactionSourceError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    return {"success": True, "data": t}


@router.delete("/{tx_id}", response_model=SuccessResponse)
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    svc = service.TransactionService(db)
    svc.delete(tx_id)
    return {"success": True, "data": {}}
