from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload

from app.modules.owners import models


class OwnerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, phone: str) -> models.Owner | None:
        statement = (
            select(models.Owner)
            .where(models.Owner.phone == phone)
            .options(
                selectinload(models.Owner.account_links).selectinload(
                    models.OwnerAccount.account
                ),
                selectinload(models.Owner.credit_card_links).selectinload(
                    models.OwnerCreditCard.credit_card
                ),
            )
        )
        return self.db.scalar(statement)

    def create(self, phone: str) -> models.Owner:
        owner = models.Owner(phone=phone)
        self.db.add(owner)
        self.db.commit()
        return self.get(phone) or owner

    def get_account_link(
        self, phone: str, account_id: int
    ) -> models.OwnerAccount | None:
        return self.db.get(models.OwnerAccount, (phone, account_id))

    def get_credit_card_link(
        self, phone: str, credit_card_id: int
    ) -> models.OwnerCreditCard | None:
        return self.db.get(models.OwnerCreditCard, (phone, credit_card_id))

    def clear_default_account(self, phone: str) -> None:
        self.db.execute(
            update(models.OwnerAccount)
            .where(models.OwnerAccount.owner_phone == phone)
            .values(is_default=False)
        )

    def clear_default_credit_card(self, phone: str) -> None:
        self.db.execute(
            update(models.OwnerCreditCard)
            .where(models.OwnerCreditCard.owner_phone == phone)
            .values(is_default=False)
        )

    def delete_account_link(self, link: models.OwnerAccount) -> None:
        self.db.delete(link)
        self.db.commit()

    def delete_credit_card_link(self, link: models.OwnerCreditCard) -> None:
        self.db.delete(link)
        self.db.commit()
