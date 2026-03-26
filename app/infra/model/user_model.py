from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.model import table_registry


@table_registry.mapped_as_dataclass
class UserModel:
    """Modelo ORM — mapeamento para a tabela 'users'."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    transactions: Mapped[List["TransactionModel"]] = relationship(  # noqa: F821
        "TransactionModel",
        back_populates="user",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )
