from uuid import UUID

from app.domain.repositories.transaction_repository import ITransactionRepository


class DeleteTransactionUseCase:
    def __init__(self, repo: ITransactionRepository) -> None:
        self._repo = repo

    async def execute(self, transaction_id: UUID) -> None:
        if not await self._repo.find_by_id(transaction_id):
            raise LookupError(f"Transação '{transaction_id}' não encontrada.")
        await self._repo.delete(transaction_id)
