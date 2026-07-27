from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.exceptions import AppException

from app.modules.accounts import models, repository, schemas


class AccountService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.AccountRepository(db)

    def create(self, payload: schemas.AccountCreate) -> models.Account:
        if payload.initial_balance < 0:
            raise AppException("Initial balance cannot be negative")
        account = models.Account(
            name=payload.name,
            institution=payload.institution,
            type=payload.type,
            initial_balance=payload.initial_balance,
            current_balance=payload.initial_balance,
            color=payload.color,
            is_active=payload.is_active,
        )
        return self.repo.create(account)

    def get(self, account_id: int) -> models.Account:
        acc = self.repo.get(account_id)
        if not acc:
            raise AppException("Account not found")
        return acc

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        active: bool | None = None,
        sort: str = "id",
        order: str = "asc",
    ):
        skip = (page - 1) * page_size
        items, total = self.repo.list(
            skip=skip, limit=page_size, active=active, sort=sort, order=order
        )
        return items, total

    def update(self, account_id: int, payload: schemas.AccountUpdate) -> models.Account:
        acc = self.get(account_id)
        if payload.name is not None:
            acc.name = payload.name
        if payload.institution is not None:
            acc.institution = payload.institution
        if payload.type is not None:
            acc.type = payload.type
        if payload.color is not None:
            acc.color = payload.color
        if payload.is_active is not None:
            acc.is_active = payload.is_active
        if payload.initial_balance is not None:
            if payload.initial_balance < 0:
                raise AppException("Initial balance cannot be negative")
            acc.initial_balance = payload.initial_balance
        if payload.current_balance is not None:
            acc.current_balance = payload.current_balance
        return self.repo.update(acc)

    def delete(self, account_id: int) -> None:
        acc = self.get(account_id)
        self.repo.delete(acc)
