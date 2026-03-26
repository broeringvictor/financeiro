from uuid import UUID

from app.application.dto.transaction_dto import TransactionResponse
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository


def _to_response(transaction: Transaction) -> TransactionResponse:
    return TransactionResponse(
        transaction_id=str(transaction.id),
        user_id=str(transaction.user_id),
        category_id=transaction.category_id,
        type=transaction.type.name,
        amount=transaction.amount.value,
        occurred_at=transaction.occurred_at.isoformat(),
        description=transaction.description,
    )


class GetTransactionUseCase:
    def __init__(self, repo: ITransactionRepository) -> None:
        self._repo = repo

    async def execute(self, transaction_id: UUID) -> TransactionResponse:
        transaction = await self._repo.find_by_id(transaction_id)
        if not transaction:
            raise LookupError(f"Transação '{transaction_id}' não encontrada.")
        return _to_response(transaction)
