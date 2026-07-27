from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.accounts.models import Account
from app.modules.credit_cards.models import CreditCard
from app.modules.owners import models, repository, schemas


class OwnerService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.OwnerRepository(db)

    def get_or_create(self, phone: str) -> models.Owner:
        normalized = schemas.normalize_phone(phone)
        return self.repo.get(normalized) or self.repo.create(normalized)

    def get(self, phone: str) -> models.Owner:
        normalized = schemas.normalize_phone(phone)
        owner = self.repo.get(normalized)
        if owner is None:
            raise AppException("Owner not found")
        return owner

    def associate_account(
        self, phone: str, account_id: int, is_default: bool = False
    ) -> models.Owner:
        normalized = schemas.normalize_phone(phone)
        if self.db.get(Account, account_id) is None:
            raise AppException("Account not found")

        self.get_or_create(normalized)
        link = self.repo.get_account_link(normalized, account_id)
        if is_default:
            self.repo.clear_default_account(normalized)
        if link is None:
            link = models.OwnerAccount(
                owner_phone=normalized,
                account_id=account_id,
                is_default=is_default,
            )
            self.db.add(link)
        else:
            link.is_default = is_default
        self.db.commit()
        return self.get(normalized)

    def associate_credit_card(
        self, phone: str, credit_card_id: int, is_default: bool = False
    ) -> models.Owner:
        normalized = schemas.normalize_phone(phone)
        if self.db.get(CreditCard, credit_card_id) is None:
            raise AppException("Credit card not found")

        self.get_or_create(normalized)
        link = self.repo.get_credit_card_link(normalized, credit_card_id)
        if is_default:
            self.repo.clear_default_credit_card(normalized)
        if link is None:
            link = models.OwnerCreditCard(
                owner_phone=normalized,
                credit_card_id=credit_card_id,
                is_default=is_default,
            )
            self.db.add(link)
        else:
            link.is_default = is_default
        self.db.commit()
        return self.get(normalized)

    def remove_account(self, phone: str, account_id: int) -> None:
        normalized = schemas.normalize_phone(phone)
        link = self.repo.get_account_link(normalized, account_id)
        if link is None:
            raise AppException("Owner account association not found")
        self.repo.delete_account_link(link)

    def remove_credit_card(self, phone: str, credit_card_id: int) -> None:
        normalized = schemas.normalize_phone(phone)
        link = self.repo.get_credit_card_link(normalized, credit_card_id)
        if link is None:
            raise AppException("Owner credit card association not found")
        self.repo.delete_credit_card_link(link)

    def get_defaults(
        self, phone: str
    ) -> tuple[models.Owner, Account | None, CreditCard | None]:
        owner = self.get(phone)
        account = next(
            (link.account for link in owner.account_links if link.is_default), None
        )
        credit_card = next(
            (
                link.credit_card
                for link in owner.credit_card_links
                if link.is_default
            ),
            None,
        )
        return owner, account, credit_card
