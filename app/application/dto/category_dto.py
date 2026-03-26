from pydantic.dataclasses import dataclass

from app.domain.enums.e_transaction import TransactionTypeEnum


@dataclass(frozen=True)
class CreateCategoryInput:
    name: str
    type: TransactionTypeEnum
    description: str | None = None


@dataclass(frozen=True)
class UpdateCategoryInput:
    category_id: int
    name: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class CategoryResponse:
    category_id: int
    name: str
    type: str
    description: str | None
