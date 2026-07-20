from typing import List as _List
from sqlalchemy.orm import Session

from app.modules.accounts import models


class AccountRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, account_id: int) -> models.Account | None:
        return self.db.query(models.Account).filter(models.Account.id == account_id).first()

    def list(self, skip: int = 0, limit: int = 20, active: bool | None = None, sort: str = "id", order: str = "asc") -> tuple[_List[models.Account], int]:
        q = self.db.query(models.Account)
        if active is not None:
            q = q.filter(models.Account.is_active == active)
        total = q.count()
        if order.lower() == "desc":
            q = q.order_by(getattr(models.Account, sort).desc())
        else:
            q = q.order_by(getattr(models.Account, sort))
        items = q.offset(skip).limit(limit).all()
        return items, total

    def create(self, account: models.Account) -> models.Account:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account: models.Account) -> models.Account:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete(self, account: models.Account) -> None:
        self.db.delete(account)
        self.db.commit()
