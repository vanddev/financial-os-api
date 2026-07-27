from decimal import Decimal

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import select

from app.core.database import get_db
from app.modules.accounts import schemas as account_schemas
from app.modules.accounts import service as account_service
from app.modules.categories import models as category_models  # noqa: F401
from app.modules.credit_cards import schemas as card_schemas
from app.modules.credit_cards import service as card_service
from app.modules.owners import router as owners_router
from app.modules.owners import service as owner_service
from app.modules.owners.models import OwnerAccount, OwnerCreditCard


def create_financial_resources(db_session):
    accounts = account_service.AccountService(db_session)
    account_one = accounts.create(
        account_schemas.AccountCreate(
            name="Conta principal",
            institution="Banco A",
            type="checking",
            initial_balance=Decimal("100.00"),
        )
    )
    account_two = accounts.create(
        account_schemas.AccountCreate(
            name="Conta reserva",
            institution="Banco B",
            type="savings",
            initial_balance=Decimal("200.00"),
        )
    )

    cards = card_service.CreditCardService(db_session)
    card_one = cards.create(
        card_schemas.CreditCardCreate(
            name="Cartão principal",
            issuer="Visa",
            last_four="1234",
            limit=Decimal("2000.00"),
        )
    )
    card_two = cards.create(
        card_schemas.CreditCardCreate(
            name="Cartão reserva",
            issuer="Mastercard",
            last_four="5678",
            limit=Decimal("3000.00"),
        )
    )
    return account_one, account_two, card_one, card_two


def test_phone_can_have_many_resources_and_only_one_default(db_session):
    account_one, account_two, card_one, card_two = create_financial_resources(
        db_session
    )
    owners = owner_service.OwnerService(db_session)

    owners.associate_account(
        "+55 (71) 99999-0001", account_one.id, is_default=True
    )
    owners.associate_account("5571999990001", account_two.id, is_default=True)
    owners.associate_credit_card("55 71 99999-0001", card_one.id, is_default=True)
    owner = owners.associate_credit_card(
        "+55 (71) 99999-0001", card_two.id, is_default=True
    )

    assert owner.phone == "5571999990001"
    assert len(owner.account_links) == 2
    assert len(owner.credit_card_links) == 2
    assert sum(link.is_default for link in owner.account_links) == 1
    assert sum(link.is_default for link in owner.credit_card_links) == 1

    _, default_account, default_card = owners.get_defaults(owner.phone)
    assert default_account is not None
    assert default_account.id == account_two.id
    assert default_card is not None
    assert default_card.id == card_two.id


def test_resource_can_belong_to_many_phones(db_session):
    account, _, card, _ = create_financial_resources(db_session)
    owners = owner_service.OwnerService(db_session)

    owners.associate_account("5571999990001", account.id, is_default=True)
    owners.associate_account("5571999990002", account.id, is_default=True)
    owners.associate_credit_card("5571999990001", card.id, is_default=True)
    owners.associate_credit_card("5571999990002", card.id, is_default=True)

    account_links = db_session.scalars(
        select(OwnerAccount).where(OwnerAccount.account_id == account.id)
    ).all()
    card_links = db_session.scalars(
        select(OwnerCreditCard).where(OwnerCreditCard.credit_card_id == card.id)
    ).all()
    assert len(account_links) == 2
    assert len(card_links) == 2


@pytest.mark.asyncio
async def test_defaults_endpoint_resolves_resources_for_whatsapp(db_session):
    account, _, card, _ = create_financial_resources(db_session)
    owners = owner_service.OwnerService(db_session)
    owners.associate_account("5571999990001", account.id, is_default=True)
    owners.associate_credit_card("5571999990001", card.id, is_default=True)

    app = FastAPI()
    app.include_router(owners_router)

    async def override_db():
        return db_session

    app.dependency_overrides[get_db] = override_db

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(
            "/owners/+55%20(71)%2099999-0001/defaults"
        )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["phone"] == "5571999990001"
    assert data["account"]["id"] == account.id
    assert data["credit_card"]["id"] == card.id


@pytest.mark.asyncio
async def test_association_endpoint_is_idempotent_and_normalizes_phone(
    db_session,
):
    account, _, _, _ = create_financial_resources(db_session)

    app = FastAPI()
    app.include_router(owners_router)

    async def override_db():
        return db_session

    app.dependency_overrides[get_db] = override_db
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        first = await client.put(
            f"/owners/5571999990001/accounts/{account.id}",
            json={"is_default": True},
        )
        second = await client.put(
            f"/owners/55%2071%2099999-0001/accounts/{account.id}",
            json={"is_default": True},
        )

    assert first.status_code == 200
    assert second.status_code == 200
    assert len(second.json()["data"]["account_links"]) == 1
