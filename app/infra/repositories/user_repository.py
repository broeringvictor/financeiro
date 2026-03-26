from uuid import UUID
from decimal import Decimal

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.enums.e_transaction import TransactionTypeEnum
from app.domain.value_objects.name import Name
from app.domain.value_objects.password import Password
from app.infra.model.transaction_model import TransactionModel
from app.infra.model.user_model import UserModel


class UserRepository:
    """
    Implementação async do UserRepository.
    Satisfaz o Protocol por estrutura — sem herança.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── persistência ──────────────────────────────────────────────────────────

    async def save(self, user: User) -> None:
        model = self._to_model(user)
        self._session.add(model)

    async def delete(self, user_id: UUID) -> None:
        model = await self._session.get(UserModel, user_id)
        if model:
            await self._session.delete(model)

    # ── consultas ─────────────────────────────────────────────────────────────

    async def find_by_id(self, user_id: UUID) -> User | None:
        model = await self._session.get(UserModel, user_id)
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.lower().strip())
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_all(self) -> list[User]:
        result = await self._session.execute(select(UserModel))
        return [self._to_entity(m) for m in result.scalars().all()]

    async def get_balance(self, user_id: UUID) -> Decimal:
        signed_amount = case(
            (TransactionModel.type == TransactionTypeEnum.INCOME.name, TransactionModel.amount),
            (TransactionModel.type == TransactionTypeEnum.EXPENSE.name, -TransactionModel.amount),
            else_=0,
        )
        result = await self._session.execute(
            select(func.coalesce(func.sum(signed_amount), 0))
            .where(TransactionModel.user_id == user_id)
        )
        return result.scalar_one()

    # ── mapeamento Entity ↔ Model ─────────────────────────────────────────────

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            name=str(user.name),
            email=str(user.email),
            hashed_password=user.password.hashed_value,
            is_active=user.is_active,
            create_at=user.create_at,
            modified_at=user.modified_at,
        )

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        parts = model.name.split()
        name = Name.model_construct(
            value=model.name,
            first_name=parts[0],
            last_name=" ".join(parts[1:]) if len(parts) > 1 else parts[0],
        )
        return User.model_construct(
            id=model.id,
            name=name,
            email=model.email,
            password=Password.from_hash(model.hashed_password),
            is_active=model.is_active,
            create_at=model.create_at,
            modified_at=model.modified_at,
        )
