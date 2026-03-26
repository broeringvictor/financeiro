from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.transaction import Transaction
from app.domain.enums.e_transaction import TransactionType
from app.domain.value_objects.amount import Amount
from app.infra.model.transaction_model import TransactionModel


class TransactionRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── persistência ──────────────────────────────────────────────────────────

    async def save(self, transaction: Transaction) -> None:
        model = self._to_model(transaction)
        self._session.add(model)

    async def update(self, transaction: Transaction) -> None:
        model = await self._session.get(TransactionModel, transaction.id)
        if not model:
            raise LookupError(f"Transação '{transaction.id}' não encontrada.")
        model.category_id = transaction.category_id
        model.type = transaction.type.name
        model.amount = transaction.amount.value
        model.description = transaction.description
        await self._session.flush()

    async def delete(self, transaction_id: UUID) -> None:
        model = await self._session.get(TransactionModel, transaction_id)
        if model:
            await self._session.delete(model)

    # ── consultas ─────────────────────────────────────────────────────────────

    async def find_by_id(self, transaction_id: UUID) -> Transaction | None:
        model = await self._session.get(TransactionModel, transaction_id)
        return self._to_entity(model) if model else None

    async def find_by_user(self, user_id: UUID) -> list[Transaction]:
        result = await self._session.execute(
            select(TransactionModel)
            .where(TransactionModel.user_id == user_id)
            .order_by(TransactionModel.occurred_at.desc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def find_by_user_and_type(
        self, user_id: UUID, type: TransactionType
    ) -> list[Transaction]:
        result = await self._session.execute(
            select(TransactionModel)
            .where(
                TransactionModel.user_id == user_id,
                TransactionModel.type == type.name,
            )
            .order_by(TransactionModel.occurred_at.desc())
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    # ── mapeamento Entity ↔ Model ─────────────────────────────────────────────

    @staticmethod
    def _to_model(transaction: Transaction) -> TransactionModel:
        return TransactionModel(
            id=transaction.id,
            user_id=transaction.user_id,
            category_id=transaction.category_id,
            type=transaction.type.name,
            amount=transaction.amount.value,
            occurred_at=transaction.occurred_at,
            description=transaction.description,
        )

    @staticmethod
    def _to_entity(model: TransactionModel) -> Transaction:
        return Transaction.model_construct(
            id=model.id,
            user_id=model.user_id,
            category_id=model.category_id,
            type=TransactionType[model.type],
            amount=Amount.from_decimal(model.amount),
            occurred_at=model.occurred_at,
            description=model.description,
        )
