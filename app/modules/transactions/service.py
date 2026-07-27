import hashlib
import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.modules.transactions import models, repository, schemas
from app.modules.transactions.source_rules import validate_transaction_source


class IdempotencyConflictError(Exception):
    pass


class TransactionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = repository.TransactionRepository(db)

    def create(
        self,
        payload: schemas.TransactionCreate,
        idempotency_key: str | None = None,
    ) -> models.Transaction:
        validate_transaction_source(
            payment_method=payload.payment_method,
            account_id=payload.account_id,
            credit_card_id=payload.credit_card_id,
        )
        if payload.installment_number and payload.installment_total:
            if payload.installment_number > payload.installment_total:
                raise AppException("installment_number cannot be greater than installment_total")

        request_hash = self._request_hash(payload) if idempotency_key else None
        if idempotency_key:
            existing = self.repo.get_by_idempotency_key(idempotency_key)
            if existing:
                return self._validate_replay(existing, request_hash)

        tx = models.Transaction(
            **payload.model_dump(),
            idempotency_key=idempotency_key,
            request_hash=request_hash,
        )
        try:
            return self.repo.create(tx)
        except IntegrityError:
            if not idempotency_key:
                raise
            existing = self.repo.get_by_idempotency_key(idempotency_key)
            if not existing:
                raise
            return self._validate_replay(existing, request_hash)

    @staticmethod
    def _request_hash(payload: schemas.TransactionCreate) -> str:
        serialized = json.dumps(
            payload.model_dump(mode="json"),
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return hashlib.sha256(serialized.encode()).hexdigest()

    @staticmethod
    def _validate_replay(
        transaction: models.Transaction,
        request_hash: str | None,
    ) -> models.Transaction:
        if transaction.request_hash != request_hash:
            raise IdempotencyConflictError
        return transaction

    def get(self, tx_id: int) -> models.Transaction:
        t = self.repo.get(tx_id)
        if not t:
            raise AppException("Transaction not found")
        return t

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict | None = None,
        sort: str = "id",
        order: str = "asc",
    ):
        skip = (page - 1) * page_size
        items, total = self.repo.list(
            skip=skip, limit=page_size, filters=filters, sort=sort, order=order
        )
        return items, total

    def update(self, tx_id: int, payload: schemas.TransactionUpdate) -> models.Transaction:
        t = self.get(tx_id)
        changes = payload.model_dump(exclude_unset=True)
        validate_transaction_source(
            payment_method=changes.get("payment_method", t.payment_method),
            account_id=changes.get("account_id", t.account_id),
            credit_card_id=changes.get("credit_card_id", t.credit_card_id),
        )
        for k, v in changes.items():
            setattr(t, k, v)
        return self.repo.update(t)

    def delete(self, tx_id: int) -> None:
        t = self.get(tx_id)
        self.repo.delete(t)
