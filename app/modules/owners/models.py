from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Owner(Base):
    __tablename__ = "owners"

    phone: Mapped[str] = mapped_column(String(15), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    account_links: Mapped[list["OwnerAccount"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    credit_card_links: Mapped[list["OwnerCreditCard"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class OwnerAccount(Base):
    __tablename__ = "owner_accounts"
    __table_args__ = (
        Index(
            "uq_owner_accounts_default_phone",
            "owner_phone",
            unique=True,
            postgresql_where=text("is_default"),
            sqlite_where=text("is_default = 1"),
        ),
    )

    owner_phone: Mapped[str] = mapped_column(
        ForeignKey("owners.phone", ondelete="CASCADE"), primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner: Mapped[Owner] = relationship(back_populates="account_links")
    account: Mapped["Account"] = relationship()  # type: ignore[name-defined]  # noqa: F821


class OwnerCreditCard(Base):
    __tablename__ = "owner_credit_cards"
    __table_args__ = (
        Index(
            "uq_owner_credit_cards_default_phone",
            "owner_phone",
            unique=True,
            postgresql_where=text("is_default"),
            sqlite_where=text("is_default = 1"),
        ),
    )

    owner_phone: Mapped[str] = mapped_column(
        ForeignKey("owners.phone", ondelete="CASCADE"), primary_key=True
    )
    credit_card_id: Mapped[int] = mapped_column(
        ForeignKey("credit_cards.id", ondelete="CASCADE"), primary_key=True
    )
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    owner: Mapped[Owner] = relationship(back_populates="credit_card_links")
    credit_card: Mapped["CreditCard"] = relationship()  # type: ignore[name-defined]  # noqa: F821
