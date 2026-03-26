from uuid import UUID

from app.application.dto.transaction_dto import TransactionResponse
from app.domain.enums.e_transaction import TransactionType
from app.domain.repositories.transaction_repository import ITransactionRepository


class GetUserTransactionsUseCase:
    def __init__(self, repo: ITransactionRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID) -> list[TransactionResponse]:
        transactions = await self._repo.find_by_user(user_id)
        return [
            TransactionResponse(
                transaction_id=str(t.id),
                user_id=str(t.user_id),
                category_id=t.category_id,
                type=t.type.name,
                amount=t.amount.value,
                occurred_at=t.occurred_at.isoformat(),
                description=t.description,
            )
            for t in transactions
        ]


class GetUserTransactionsByTypeUseCase:
    def __init__(self, repo: ITransactionRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID, type: TransactionType) -> list[TransactionResponse]:
        transactions = await self._repo.find_by_user_and_type(user_id, type)
        return [
            TransactionResponse(
                transaction_id=str(t.id),
                user_id=str(t.user_id),
                category_id=t.category_id,
                type=t.type.name,
                amount=t.amount.value,
                occurred_at=t.occurred_at.isoformat(),
                description=t.description,
            )
            for t in transactions
        ]
