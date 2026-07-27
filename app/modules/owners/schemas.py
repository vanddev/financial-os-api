import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.shared.domain_enums import AccountType


def normalize_phone(phone: str) -> str:
    if re.fullmatch(r"[+\d\s().-]+", phone) is None:
        raise ValueError("Phone contains invalid characters")
    normalized = re.sub(r"\D", "", phone)
    if not 8 <= len(normalized) <= 15:
        raise ValueError("Phone must contain between 8 and 15 digits")
    return normalized


class PhoneSchema(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        return normalize_phone(value)


class OwnerCreate(PhoneSchema):
    pass


class AssociationUpdate(BaseModel):
    is_default: bool = False


class AccountSummary(BaseModel):
    id: int
    name: str
    institution: str | None
    type: AccountType
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CreditCardSummary(BaseModel):
    id: int
    name: str
    issuer: str | None
    last_four: str | None
    active: bool

    model_config = ConfigDict(from_attributes=True)


class OwnerAccountOut(BaseModel):
    is_default: bool
    account: AccountSummary

    model_config = ConfigDict(from_attributes=True)


class OwnerCreditCardOut(BaseModel):
    is_default: bool
    credit_card: CreditCardSummary

    model_config = ConfigDict(from_attributes=True)


class OwnerOut(PhoneSchema):
    account_links: list[OwnerAccountOut]
    credit_card_links: list[OwnerCreditCardOut]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OwnerDefaultsOut(PhoneSchema):
    account: AccountSummary | None
    credit_card: CreditCardSummary | None
