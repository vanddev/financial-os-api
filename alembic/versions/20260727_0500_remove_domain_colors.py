"""Remove presentation colors from domain tables.

Revision ID: remove_domain_colors
Revises: transaction_source_rules
"""

import sqlalchemy as sa

from alembic import op

revision = "remove_domain_colors"
down_revision = "transaction_source_rules"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("accounts", "color")
    op.drop_column("categories", "color")
    op.drop_column("goals", "color")


def downgrade() -> None:
    op.add_column(
        "goals",
        sa.Column("color", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "categories",
        sa.Column("color", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "accounts",
        sa.Column("color", sa.String(length=20), nullable=True),
    )
