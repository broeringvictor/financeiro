from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID8

from app.domain.enums.e_transaction import TransactionType


class Transaction(BaseModel):
    id: UUID8
    user_id: UUID8
    category_id: int
    type: TransactionType
    description: str | None = None
    amount: Decimal
    occurred_at: datetime
