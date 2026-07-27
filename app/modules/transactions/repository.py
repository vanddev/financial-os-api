from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.transactions import models


class TransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, transaction_id: int) -> models.Transaction | None:
        return self.db.scalar(
            select(models.Transaction).where(models.Transaction.id == transaction_id)
        )

    def get_by_idempotency_key(self, idempotency_key: str) -> models.Transaction | None:
        return self.db.scalar(
            select(models.Transaction).where(models.Transaction.idempotency_key == idempotency_key)
        )

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        filters: dict | None = None,
        sort: str = "id",
        order: str = "asc",
    ) -> tuple[list[models.Transaction], int]:
        q = self.db.query(models.Transaction)
        if filters:
            if filters.get("account_id"):
                q = q.filter(models.Transaction.account_id == filters["account_id"])
            if filters.get("category_id"):
                q = q.filter(models.Transaction.category_id == filters["category_id"])
            if filters.get("credit_card_id"):
                q = q.filter(models.Transaction.credit_card_id == filters["credit_card_id"])
            if filters.get("status"):
                q = q.filter(models.Transaction.status == filters["status"])
            if filters.get("transaction_type"):
                q = q.filter(
                    models.Transaction.transaction_type == filters["transaction_type"]
                )
            if filters.get("description"):
                q = q.filter(models.Transaction.description.ilike(f"%{filters['description']}%"))
            if filters.get("min_amount") is not None:
                q = q.filter(models.Transaction.amount >= filters["min_amount"])
            if filters.get("max_amount") is not None:
                q = q.filter(models.Transaction.amount <= filters["max_amount"])
            if filters.get("start_date"):
                q = q.filter(models.Transaction.transaction_date >= filters["start_date"])
            if filters.get("end_date"):
                q = q.filter(models.Transaction.transaction_date <= filters["end_date"])
        total = q.count()
        if order.lower() == "desc":
            q = q.order_by(getattr(models.Transaction, sort).desc())
        else:
            q = q.order_by(getattr(models.Transaction, sort))
        items = q.offset(skip).limit(limit).all()
        return items, total

    def create(self, tx: models.Transaction) -> models.Transaction:
        self.db.add(tx)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(tx)
        return tx

    def update(self, tx: models.Transaction) -> models.Transaction:
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def delete(self, tx: models.Transaction) -> None:
        self.db.delete(tx)
        self.db.commit()
