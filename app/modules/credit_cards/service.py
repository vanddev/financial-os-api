from sqlalchemy.orm import Session
from app.core.exceptions import AppException

from app.modules.credit_cards import models, repository, schemas


class CreditCardService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.CreditCardRepository(db)

    def create(self, payload: schemas.CreditCardCreate) -> models.CreditCard:
        if payload.limit < 0:
            raise AppException("Credit card limit cannot be negative")
        card = models.CreditCard(**payload.model_dump())
        return self.repo.create(card)

    def get(self, card_id: int) -> models.CreditCard:
        c = self.repo.get(card_id)
        if not c:
            raise AppException("Credit card not found")
        return c

    def list(self, page: int = 1, page_size: int = 20, active: bool | None = None, sort: str = "id", order: str = "asc"):
        skip = (page - 1) * page_size
        items, total = self.repo.list(skip=skip, limit=page_size, active=active, sort=sort, order=order)
        return items, total

    def update(self, card_id: int, payload: schemas.CreditCardUpdate) -> models.CreditCard:
        c = self.get(card_id)
        for k, v in payload.model_dump().items():
            setattr(c, k, v)
        return self.repo.update(c)

    def delete(self, card_id: int) -> None:
        c = self.get(card_id)
        self.repo.delete(c)
