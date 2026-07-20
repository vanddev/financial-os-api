from typing import List as _List
from sqlalchemy.orm import Session

from app.modules.credit_cards import models


class CreditCardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, card_id: int) -> models.CreditCard | None:
        return self.db.query(models.CreditCard).filter(models.CreditCard.id == card_id).first()

    def list(self, skip: int = 0, limit: int = 20, active: bool | None = None, sort: str = "id", order: str = "asc") -> tuple[_List[models.CreditCard], int]:
        q = self.db.query(models.CreditCard)
        if active is not None:
            q = q.filter(models.CreditCard.active == active)
        total = q.count()
        if order.lower() == "desc":
            q = q.order_by(getattr(models.CreditCard, sort).desc())
        else:
            q = q.order_by(getattr(models.CreditCard, sort))
        items = q.offset(skip).limit(limit).all()
        return items, total

    def create(self, card: models.CreditCard) -> models.CreditCard:
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def update(self, card: models.CreditCard) -> models.CreditCard:
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def delete(self, card: models.CreditCard) -> None:
        self.db.delete(card)
        self.db.commit()
