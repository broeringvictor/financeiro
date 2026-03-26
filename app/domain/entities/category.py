from pydantic import BaseModel

from app.domain.value_objects.transaction_type import TransactionType


class Category(BaseModel):
    id: int | None = None
    name: str
    type: TransactionType
    description: str | None = None

    @classmethod
    def create(
        cls,
        name: str,
        type: TransactionType | str | int,
        description: str | None = None,
    ) -> "Category":
        name = name.strip()
        if not name:
            raise ValueError("Category name cannot be empty.")
        return cls(
            name=name,
            type=TransactionType.create(type),
            description=description,
        )

    def update(
        self,
        name: str | None = None,
        description: str | None = None,
    ) -> None:
        if name is not None:
            name = name.strip()
            if not name:
                raise ValueError("Category name cannot be empty.")
            self.name = name
        if description is not None:
            self.description = description
