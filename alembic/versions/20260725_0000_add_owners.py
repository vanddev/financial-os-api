"""Add phone owners and account/card associations.

Revision ID: add_phone_owners
Revises: remove_credit_card_color
"""

import sqlalchemy as sa

from alembic import op

revision = "add_phone_owners"
down_revision = "remove_credit_card_color"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "owners",
        sa.Column("phone", sa.String(length=15), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("phone"),
    )
    op.create_table(
        "owner_accounts",
        sa.Column("owner_phone", sa.String(length=15), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column(
            "is_default",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["owner_phone"], ["owners.phone"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("owner_phone", "account_id"),
    )
    op.create_index(
        "uq_owner_accounts_default_phone",
        "owner_accounts",
        ["owner_phone"],
        unique=True,
        postgresql_where=sa.text("is_default"),
        sqlite_where=sa.text("is_default = 1"),
    )
    op.create_table(
        "owner_credit_cards",
        sa.Column("owner_phone", sa.String(length=15), nullable=False),
        sa.Column("credit_card_id", sa.Integer(), nullable=False),
        sa.Column(
            "is_default",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["credit_card_id"], ["credit_cards.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["owner_phone"], ["owners.phone"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("owner_phone", "credit_card_id"),
    )
    op.create_index(
        "uq_owner_credit_cards_default_phone",
        "owner_credit_cards",
        ["owner_phone"],
        unique=True,
        postgresql_where=sa.text("is_default"),
        sqlite_where=sa.text("is_default = 1"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_owner_credit_cards_default_phone",
        table_name="owner_credit_cards",
    )
    op.drop_table("owner_credit_cards")
    op.drop_index(
        "uq_owner_accounts_default_phone", table_name="owner_accounts"
    )
    op.drop_table("owner_accounts")
    op.drop_table("owners")
