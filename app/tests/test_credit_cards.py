from decimal import Decimal

from app.modules.credit_cards import service as card_service, schemas as card_schemas


def test_credit_cards_crud(db_session):
    svc = card_service.CreditCardService(db_session)
    payload = card_schemas.CreditCardCreate(name="Card1", issuer="Visa", last_four="1234", limit=Decimal("2000.00"), closing_day=20, due_day=5, color="#000")
    c = svc.create(payload)
    assert c.id is not None
    got = svc.get(c.id)
    assert got.name == "Card1"
    svc.update(c.id, card_schemas.CreditCardUpdate(name="CardX", issuer="Visa", last_four="1234", limit=Decimal("3000.00"), closing_day=20, due_day=5, color="#000", active=False))
    got2 = svc.get(c.id)
    assert got2.name == "CardX"
    svc.delete(c.id)
    try:
        svc.get(c.id)
        assert False
    except Exception:
        assert True
