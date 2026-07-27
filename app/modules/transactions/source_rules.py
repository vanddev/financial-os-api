from app.shared.domain_enums import PaymentMethod

ACCOUNT_REQUIRED_METHODS = frozenset(
    {
        PaymentMethod.DEBIT_CARD,
        PaymentMethod.PIX,
        PaymentMethod.BANK_TRANSFER,
        PaymentMethod.AUTOMATIC_DEBIT,
    }
)


class TransactionSourceError(ValueError):
    pass


def validate_transaction_source(
    *,
    payment_method: PaymentMethod | str | None,
    account_id: int | None,
    credit_card_id: int | None,
) -> None:
    if account_id is not None and credit_card_id is not None:
        raise TransactionSourceError("account_id and credit_card_id cannot be provided together")

    if payment_method == PaymentMethod.CREDIT_CARD and credit_card_id is None:
        raise TransactionSourceError(
            "credit_card_id is required when payment_method is credit_card"
        )

    if payment_method in ACCOUNT_REQUIRED_METHODS and account_id is None:
        raise TransactionSourceError(
            f"account_id is required when payment_method is {payment_method}"
        )
