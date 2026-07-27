from decimal import Decimal

from app.modules.accounts import schemas, service


def test_account_crud(db_session):
    svc = service.AccountService(db_session)
    payload = schemas.AccountCreate(
        name="Test Account", institution="Bank", type="checking", initial_balance=Decimal("100.00")
    )
    acc = svc.create(payload)
    assert acc.id is not None
    got = svc.get(acc.id)
    assert got.name == "Test Account"
    # update
    upd = schemas.AccountUpdate(
        name="Updated", institution="Bank", type="checking", is_active=False
    )
    svc.update(acc.id, upd)
    got2 = svc.get(acc.id)
    assert got2.name == "Updated"
    svc.delete(acc.id)
    try:
        svc.get(acc.id)
        assert False, "Expected exception for missing account"
    except Exception:
        assert True
