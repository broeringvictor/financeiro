from uuid import UUID

from app.application.dto.transaction_dto import (
    TransactionResponse,
    UpdateTransactionInput,
)
from app.domain.repositories.transaction_repository import ITransactionRepository


class UpdateTransactionUseCase:
    def __init__(self, repo: ITransactionRepository) -> None:
        self._repo = repo

    async def execute(self, input_data: UpdateTransactionInput) -> TransactionResponse:
        transaction_id = UUID(input_data.transaction_id)
        transaction = await self._repo.find_by_id(transaction_id)
        if not transaction:
            raise LookupError(
                f"Transação '{input_data.transaction_id}' não encontrada."
            )

        transaction.update(
            category_id=input_data.category_id,
            type=input_data.type,
            amount=input_data.amount,
            description=input_data.description,
        )
        await self._repo.update(transaction)

        return TransactionResponse(
            transaction_id=str(transaction.id),
            user_id=str(transaction.user_id),
            category_id=transaction.category_id,
            type=transaction.type.name,
            amount=transaction.amount.value,
            occurred_at=transaction.occurred_at.isoformat(),
            description=transaction.description,
        )
