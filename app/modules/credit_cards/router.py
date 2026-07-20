from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.credit_cards import schemas, service
from app.modules.credit_cards.dto import CreditCardDTO
from app.modules.credit_cards.schemas import (
    CreditCardBiggestPurchaseItem,
    CreditCardCategoryBreakdownItem,
    CreditCardInstallmentItem,
)
from app.shared.pagination.paginator import PageResponse
from app.shared.responses.api import SuccessResponse
from app.shared.responses.schemas import HistoricalValue

router = APIRouter(prefix="/credit-cards", tags=["credit_cards"])


@router.get("/installments", response_model=SuccessResponse[list[CreditCardInstallmentItem]])
def get_credit_card_installments(db: Session = Depends(get_db)):
    from sqlalchemy import desc

    from app.modules.transactions.models import Transaction

    # Query all credit card transactions with installment info
    txs = (
        db.query(Transaction)
        .filter(
            Transaction.credit_card_id.is_not(None),
            Transaction.installment_number.is_not(None),
            Transaction.installment_total.is_not(None),
        )
        .order_by(Transaction.description, desc(Transaction.installment_number))
        .all()
    )

    seen_descriptions = set()
    installments_list = []
    for tx in txs:
        if tx.description in seen_descriptions:
            continue
        seen_descriptions.add(tx.description)

        remaining = tx.installment_total - tx.installment_number
        if remaining > 0:
            next_due = tx.transaction_date + timedelta(days=30)
            installments_list.append(
                {
                    "description": tx.description,
                    "remaining_installments": remaining,
                    "monthly_value": float(abs(tx.amount)),
                    "next_due": next_due.strftime("%Y-%m-%d"),
                }
            )

    if not installments_list:
        installments_list = [
            {
                "description": 'Monitor LG 27"',
                "remaining_installments": 8,
                "monthly_value": 219.9,
                "next_due": "2025-08-02",
            },
            {
                "description": "Board Game — Ark Nova",
                "remaining_installments": 3,
                "monthly_value": 91.65,
                "next_due": "2025-08-12",
            },
            {
                "description": "Capa iPhone",
                "remaining_installments": 2,
                "monthly_value": 49.9,
                "next_due": "2025-08-04",
            },
        ]

    return {"success": True, "data": installments_list}


@router.get("/", response_model=SuccessResponse[PageResponse[CreditCardDTO]])
def list_cards(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    active: bool | None = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    svc = service.CreditCardService(db)
    items, total = svc.list(page=page, page_size=page_size, active=active, sort=sort, order=order)

    start_date = datetime(2025, 7, 1)
    end_date = datetime(2025, 7, 31, 23, 59, 59)

    enriched_items = []
    from app.modules.transactions.models import Transaction

    for item in items:
        current_bill = db.query(func.sum(Transaction.amount)).filter(
            Transaction.credit_card_id == item.id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.status == "cleared",
        ).scalar() or Decimal("0.00")

        current_bill = abs(current_bill)
        available = item.limit - current_bill
        utilization = Decimal("0.00")
        if item.limit > 0:
            utilization = (current_bill / item.limit) * 100

        item.current_bill = current_bill
        item.available = available
        item.utilization = utilization
        enriched_items.append(item)

    return {
        "success": True,
        "data": {"items": enriched_items, "page": page, "page_size": page_size, "total": total},
    }


@router.get("/{card_id}/spending-history", response_model=SuccessResponse[list[HistoricalValue]])
def get_card_spending_history(card_id: int, db: Session = Depends(get_db)):
    from collections import defaultdict

    from app.modules.transactions.models import Transaction

    txs = (
        db.query(Transaction)
        .filter(
            Transaction.credit_card_id == card_id,
            Transaction.transaction_type == "expense",
            Transaction.status == "cleared",
        )
        .all()
    )

    monthly_sums = defaultdict(Decimal)
    for tx in txs:
        date = tx.transaction_date
        monthly_sums[(date.year, date.month)] += abs(tx.amount)

    months_keys = [(2025, 7), (2025, 6), (2025, 5), (2025, 4), (2025, 3), (2025, 2)]

    month_names = {2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun", 7: "Jul"}

    result = []
    for y, m in reversed(months_keys):
        result.append(
            {"month": month_names[m], "value": float(monthly_sums.get((y, m), Decimal("0.00")))}
        )

    return {"success": True, "data": result}


@router.get(
    "/{card_id}/category-breakdown",
    response_model=SuccessResponse[list[CreditCardCategoryBreakdownItem]],
)
def get_card_category_breakdown(card_id: int, db: Session = Depends(get_db)):
    from app.modules.categories.models import Category
    from app.modules.transactions.models import Transaction

    start_date = datetime(2025, 7, 1)
    end_date = datetime(2025, 7, 31, 23, 59, 59)

    results = (
        db.query(Category.name, Category.color, func.sum(Transaction.amount).label("total"))
        .join(Transaction, Transaction.category_id == Category.id)
        .filter(
            Transaction.credit_card_id == card_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
        )
        .group_by(Category.id)
        .all()
    )

    data = []
    for name, color, total in results:
        data.append({"name": name, "value": float(abs(total)), "color": color})

    if not data:
        if card_id == 1:
            data = [
                {"name": "Alimentação", "value": 1240, "color": "var(--chart-1)"},
                {"name": "Viagem", "value": 1980, "color": "var(--chart-2)"},
                {"name": "Compras", "value": 1650, "color": "var(--chart-3)"},
                {"name": "Assinaturas", "value": 240, "color": "var(--chart-4)"},
                {"name": "Outros", "value": 1300, "color": "var(--chart-5)"},
            ]
        else:
            data = [
                {"name": "Mercado", "value": 180, "color": "var(--chart-1)"},
                {"name": "Combustível", "value": 120, "color": "var(--chart-2)"},
                {"name": "Streaming", "value": 90, "color": "var(--chart-3)"},
                {"name": "Outros", "value": 42, "color": "var(--chart-4)"},
            ]

    return {"success": True, "data": data}


@router.get(
    "/{card_id}/biggest-purchases",
    response_model=SuccessResponse[list[CreditCardBiggestPurchaseItem]],
)
def get_card_biggest_purchases(card_id: int, db: Session = Depends(get_db)):
    from app.modules.transactions.models import Transaction

    start_date = datetime(2025, 7, 1)
    end_date = datetime(2025, 7, 31, 23, 59, 59)

    txs = (
        db.query(Transaction)
        .filter(
            Transaction.credit_card_id == card_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
        )
        .order_by(Transaction.amount)
        .limit(5)
        .all()
    )

    data = []
    for tx in txs:
        data.append(
            {
                "description": tx.description,
                "amount": float(abs(tx.amount)),
                "date": tx.transaction_date.strftime("%d/%b"),
            }
        )

    if not data:
        if card_id == 1:
            data = [
                {"description": 'Monitor LG 27"', "amount": 2199, "date": "02/Jul"},
                {"description": "Restaurante — Fasano", "amount": 412, "date": "08/Jul"},
                {"description": "Passagem — GRU→SDU", "amount": 890, "date": "21/Jun"},
            ]
        else:
            data = [
                {"description": "Combustível — Shell", "amount": 320, "date": "06/Jul"},
                {"description": "Board Game — Ark Nova", "amount": 91.65, "date": "12/Jul"},
            ]

    return {"success": True, "data": data}


@router.post("/", response_model=SuccessResponse[CreditCardDTO])
def create_card(payload: schemas.CreditCardCreate, db: Session = Depends(get_db)):
    svc = service.CreditCardService(db)
    c = svc.create(payload)
    return {"success": True, "data": c}


@router.get("/{card_id}", response_model=SuccessResponse[CreditCardDTO])
def get_card(card_id: int, db: Session = Depends(get_db)):
    svc = service.CreditCardService(db)
    c = svc.get(card_id)
    return {"success": True, "data": c}


@router.put("/{card_id}", response_model=SuccessResponse[CreditCardDTO])
def update_card(card_id: int, payload: schemas.CreditCardUpdate, db: Session = Depends(get_db)):
    svc = service.CreditCardService(db)
    c = svc.update(card_id, payload)
    return {"success": True, "data": c}


@router.delete("/{card_id}", response_model=SuccessResponse)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    svc = service.CreditCardService(db)
    svc.delete(card_id)
    return {"success": True, "data": {}}
