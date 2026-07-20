from datetime import datetime
from decimal import Decimal

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.database import get_db
from app.modules.accounts import schemas as acc_schemas
from app.modules.accounts import service as acc_service
from app.modules.categories import schemas as cat_schemas
from app.modules.categories import service as cat_service
from app.modules.credit_cards import models as credit_card_models  # noqa: F401
from app.modules.transactions import (
    router as transactions_router,
)
from app.modules.transactions import (
    schemas as tx_schemas,
)
from app.modules.transactions import (
    service as tx_service,
)


def test_transactions_crud(db_session):
    acc_svc = acc_service.AccountService(db_session)
    acc = acc_svc.create(acc_schemas.AccountCreate(name="TxAcct", institution="B", type="checking", initial_balance=Decimal("500")))
    cat_svc = cat_service.CategoryService(db_session)
    cat = cat_svc.create(cat_schemas.CategoryCreate(name="TxCat", color="#111", icon="i", type="expense"))
    txs = tx_service.TransactionService(db_session)
    payload = tx_schemas.TransactionCreate(account_id=acc.id, category_id=cat.id, amount=Decimal("-50.00"), transaction_type="expense", transaction_date=datetime.utcnow())
    tx = txs.create(payload)
    assert tx.id is not None
    got = txs.get(tx.id)
    assert got.amount == payload.amount
    txs.update(tx.id, tx_schemas.TransactionUpdate(account_id=acc.id, category_id=cat.id, amount=Decimal("-30.00"), transaction_type="expense", transaction_date=datetime.utcnow()))
    got2 = txs.get(tx.id)
    assert got2.amount == Decimal("-30.00")
    txs.delete(tx.id)
    try:
        txs.get(tx.id)
        assert False
    except Exception:
        assert True


def test_create_transaction_serializes_orm_model(db_session):
    account = acc_service.AccountService(db_session).create(
        acc_schemas.AccountCreate(
            name="API TxAcct",
            institution="B",
            type="checking",
            initial_balance=Decimal("500"),
        )
    )
    category = cat_service.CategoryService(db_session).create(
        cat_schemas.CategoryCreate(
            name="API TxCat",
            color="#111",
            icon="i",
            type="expense",
        )
    )

    app = FastAPI()
    app.include_router(transactions_router)
    app.dependency_overrides[get_db] = lambda: db_session

    response = TestClient(app).post(
        "/transactions/",
        json={
            "account_id": account.id,
            "category_id": category.id,
            "amount": -54,
            "transaction_type": "expense",
            "transaction_date": "2026-07-20T00:00:00",
            "credit_card_id": None,
            "description": "Teste",
            "payment_method": "Débito",
            "status": "cleared",
            "installment_number": None,
            "installment_total": None,
            "notes": None,
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["amount"] == -54.0
    assert response.json()["data"]["description"] == "Teste"
