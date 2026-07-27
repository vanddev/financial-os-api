"""Add idempotency metadata to transactions.

Revision ID: add_transaction_idempotency
Revises: add_phone_owners
"""

import sqlalchemy as sa

from alembic import op

revision = "add_transaction_idempotency"
down_revision = "add_phone_owners"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("request_hash", sa.String(length=64), nullable=True),
    )
    op.create_unique_constraint(
        "uq_transactions_idempotency_key",
        "transactions",
        ["idempotency_key"],
    )
    op.create_check_constraint(
        "ck_transactions_idempotency_pair",
        "transactions",
        "(idempotency_key IS NULL AND request_hash IS NULL) OR "
        "(idempotency_key IS NOT NULL AND request_hash IS NOT NULL)",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_transactions_idempotency_pair",
        "transactions",
        type_="check",
    )
    op.drop_constraint(
        "uq_transactions_idempotency_key",
        "transactions",
        type_="unique",
    )
    op.drop_column("transactions", "request_hash")
    op.drop_column("transactions", "idempotency_key")
