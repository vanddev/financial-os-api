"""Remove color from credit cards.

Revision ID: remove_credit_card_color
Revises: repair_missing_schema
"""

import sqlalchemy as sa

from alembic import op

revision = "remove_credit_card_color"
down_revision = "repair_missing_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("credit_cards", "color")


def downgrade() -> None:
    op.add_column("credit_cards", sa.Column("color", sa.String(length=20), nullable=True))
