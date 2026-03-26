from pydantic import BaseModel

from app.domain.enums.e_transaction import TransactionType


class Category(BaseModel):
    """
    Represents a category entity.
    """

    id: int
    name: str
    type: TransactionType
    description: str | None = None
