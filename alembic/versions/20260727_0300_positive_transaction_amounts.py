"""Store transaction amounts as positive magnitudes.

Revision ID: positive_transaction_amounts
Revises: remove_brokerage_payment_method
"""

from alembic import op

revision = "positive_transaction_amounts"
down_revision = "remove_brokerage_payment_method"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE transactions SET amount = ABS(amount)")
    op.create_check_constraint(
        "ck_transactions_amount_positive",
        "transactions",
        "amount > 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_transactions_amount_positive",
        "transactions",
        type_="check",
    )
    op.execute(
        """
        UPDATE transactions
        SET amount = -amount
        WHERE transaction_type = 'expense'
        """
    )
