"""Allow account-less card transactions and enforce source rules.

Revision ID: transaction_source_rules
Revises: positive_transaction_amounts
"""

from alembic import op

revision = "transaction_source_rules"
down_revision = "positive_transaction_amounts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("transactions", "account_id", nullable=True)

    op.execute(
        """
        UPDATE transactions
        SET payment_method = 'other'
        WHERE payment_method = 'credit_card'
          AND credit_card_id IS NULL
        """
    )
    op.execute(
        """
        UPDATE transactions
        SET account_id = NULL
        WHERE payment_method = 'credit_card'
          AND credit_card_id IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE transactions
        SET payment_method = 'other'
        WHERE payment_method IN (
            'debit_card',
            'pix',
            'bank_transfer',
            'automatic_debit'
        )
          AND account_id IS NULL
        """
    )
    op.execute(
        """
        UPDATE transactions
        SET credit_card_id = NULL
        WHERE payment_method IN (
            'debit_card',
            'pix',
            'bank_transfer',
            'automatic_debit'
        )
          AND account_id IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE transactions
        SET account_id = NULL
        WHERE account_id IS NOT NULL
          AND credit_card_id IS NOT NULL
        """
    )

    op.create_check_constraint(
        "ck_transactions_single_source",
        "transactions",
        "account_id IS NULL OR credit_card_id IS NULL",
    )
    op.create_check_constraint(
        "ck_transactions_credit_card_source",
        "transactions",
        "payment_method != 'credit_card' OR (credit_card_id IS NOT NULL AND account_id IS NULL)",
    )
    op.create_check_constraint(
        "ck_transactions_account_source",
        "transactions",
        "payment_method NOT IN "
        "('debit_card', 'pix', 'bank_transfer', 'automatic_debit') OR "
        "(account_id IS NOT NULL AND credit_card_id IS NULL)",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_transactions_account_source",
        "transactions",
        type_="check",
    )
    op.drop_constraint(
        "ck_transactions_credit_card_source",
        "transactions",
        type_="check",
    )
    op.drop_constraint(
        "ck_transactions_single_source",
        "transactions",
        type_="check",
    )
    # account_id remains nullable because card purchases have no safe bank
    # account to restore during downgrade.
