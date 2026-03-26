from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infra.model import table_registry

if TYPE_CHECKING:
    from app.infra.model.user_model import UserModel


@table_registry.mapped_as_dataclass
class TransactionModel:
    """Modelo ORM — mapeamento para a tabela 'user_transactions'."""

    __tablename__ = "transactions"
    __table_args__ = (
        Index(
            "ix_user_transactions_user_occurred", "user_id", text("occurred_at DESC")
        ),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=2), nullable=False
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="transactions", init=False
    )  # type: ignore[misc]
