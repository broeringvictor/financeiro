from pydantic import BaseModel

from app.domain.enums.e_transaction import TransactionType


class Category(BaseModel):
    id: int | None = None
    name: str
    type: TransactionType
    description: str | None = None

    @classmethod
    def create(
        cls,
        name: str,
        type: TransactionType,
        description: str | None = None,
    ) -> "Category":
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        return cls(
            name=name,
            type=type,
            description=description,
        )
