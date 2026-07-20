from sqlalchemy.orm import Session
from app.core.exceptions import AppException

from app.modules.transactions import models, repository, schemas


class TransactionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.TransactionRepository(db)

    def create(self, payload: schemas.TransactionCreate) -> models.Transaction:
        if payload.installment_number and payload.installment_total:
            if payload.installment_number > payload.installment_total:
                raise AppException("installment_number cannot be greater than installment_total")
        tx = models.Transaction(**payload.model_dump())
        return self.repo.create(tx)

    def get(self, tx_id: int) -> models.Transaction:
        t = self.repo.get(tx_id)
        if not t:
            raise AppException("Transaction not found")
        return t

    def list(self, page: int = 1, page_size: int = 20, filters: dict | None = None, sort: str = "id", order: str = "asc"):
        skip = (page - 1) * page_size
        items, total = self.repo.list(skip=skip, limit=page_size, filters=filters, sort=sort, order=order)
        return items, total

    def update(self, tx_id: int, payload: schemas.TransactionUpdate) -> models.Transaction:
        t = self.get(tx_id)
        for k, v in payload.model_dump().items():
            setattr(t, k, v)
        return self.repo.update(t)

    def delete(self, tx_id: int) -> None:
        t = self.get(tx_id)
        self.repo.delete(t)
