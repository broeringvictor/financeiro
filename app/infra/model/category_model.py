from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums.e_transaction import TransactionTypeEnum
from app.infra.model import table_registry


@table_registry.mapped_as_dataclass
class CategoryModel:
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False,
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    type: Mapped[TransactionTypeEnum] = mapped_column(
        Enum(TransactionTypeEnum), nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default=None
    )
