from enum import StrEnum


class AccountType(StrEnum):
    CHECKING = "checking"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    CASH = "cash"


class CashFlowType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class PaymentMethod(StrEnum):
    CASH = "cash"
    PIX = "pix"
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    AUTOMATIC_DEBIT = "automatic_debit"
    BANK_SLIP = "bank_slip"
    OTHER = "other"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    CLEARED = "cleared"
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"


class AssetType(StrEnum):
    REAL_ESTATE = "real_estate"
    VEHICLE = "vehicle"
    MOTORCYCLE = "motorcycle"
    COLLECTIBLE = "collectible"
    ELECTRONICS = "electronics"
    CASH = "cash"
    OTHER = "other"


class InvestmentType(StrEnum):
    STOCK = "stock"
    ETF = "etf"
    TREASURY_BOND = "treasury_bond"
    CRYPTOCURRENCY = "cryptocurrency"
    FIXED_INCOME = "fixed_income"
    FUND = "fund"
    OTHER = "other"


class LoanType(StrEnum):
    MORTGAGE = "mortgage"
    VEHICLE = "vehicle"
    PERSONAL = "personal"
    PAYROLL = "payroll"
    OTHER = "other"
