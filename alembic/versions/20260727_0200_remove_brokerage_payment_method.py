"""Replace brokerage payment method with bank transfer.

Revision ID: remove_brokerage_payment_method
Revises: normalize_domain_values
"""

from alembic import op

revision = "remove_brokerage_payment_method"
down_revision = "normalize_domain_values"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE transactions
        SET payment_method = 'bank_transfer'
        WHERE payment_method = 'brokerage'
        """
    )


def downgrade() -> None:
    # The conversion is intentionally irreversible: after normalization there
    # is no reliable way to distinguish former brokerage rows from genuine
    # bank transfers.
    pass
