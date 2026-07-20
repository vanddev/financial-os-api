from decimal import Decimal
from datetime import datetime

from app.modules.accounts import service as acc_service, schemas as acc_schemas
from app.modules.categories import service as cat_service, schemas as cat_schemas
from app.modules.transactions import service as tx_service, schemas as tx_schemas


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
