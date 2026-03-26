from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid8

from pydantic import BaseModel, UUID8, Field

from app.domain.enums.e_transaction import TransactionType
from app.domain.value_objects.amount import Amount


class Transaction(BaseModel):
    id: UUID8 = Field(default_factory=uuid8)
    user_id: UUID8
    category_id: int
    type: TransactionType
    amount: Amount
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    description: str | None = None

    @classmethod
    def create(
        cls,
        user_id: UUID8,
        category_id: int,
        type: TransactionType,
        amount: Decimal | int | float | str,
        description: str | None = None,
    ) -> "Transaction":
        return cls(
            user_id=user_id,
            category_id=category_id,
            type=type,
            amount=Amount.create(amount),
            description=description,
        )

    def update(
        self,
        category_id: int | None = None,
        type: TransactionType | None = None,
        amount: Decimal | int | float | str | None = None,
        description: str | None = None,
    ) -> None:
        if category_id is not None:
            self.category_id = category_id
        if type is not None:
            self.type = type
        if amount is not None:
            self.amount = Amount.create(amount)
        if description is not None:
            self.description = description
