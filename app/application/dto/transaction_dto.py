from decimal import Decimal

from pydantic.dataclasses import dataclass

from app.domain.enums.e_transaction import TransactionType


@dataclass(frozen=True)
class CreateTransactionInput:
    user_id: str
    category_id: int
    type: TransactionType
    amount: Decimal
    description: str | None = None


@dataclass(frozen=True)
class UpdateTransactionInput:
    transaction_id: str
    category_id: int | None = None
    type: TransactionType | None = None
    amount: Decimal | None = None
    description: str | None = None


@dataclass(frozen=True)
class TransactionResponse:
    transaction_id: str
    user_id: str
    category_id: int
    type: str
    amount: Decimal
    occurred_at: str
    description: str | None
