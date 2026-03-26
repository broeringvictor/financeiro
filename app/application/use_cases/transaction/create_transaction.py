from uuid import UUID

from app.application.dto.transaction_dto import CreateTransactionInput, TransactionResponse
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.repositories.user_repository import IUserRepository


class CreateTransactionUseCase:
    def __init__(self, transaction_repo: ITransactionRepository, user_repo: IUserRepository) -> None:
        self._transaction_repo = transaction_repo
        self._user_repo = user_repo

    async def execute(self, input_data: CreateTransactionInput) -> TransactionResponse:
        user_id = UUID(input_data.user_id)

        if not await self._user_repo.find_by_id(user_id):
            raise LookupError(f"Usuário '{input_data.user_id}' não encontrado.")

        transaction = Transaction.create(
            user_id=user_id,
            category_id=input_data.category_id,
            type=input_data.type,
            amount=input_data.amount,
            description=input_data.description,
        )
        await self._transaction_repo.save(transaction)

        return TransactionResponse(
            transaction_id=str(transaction.id),
            user_id=str(transaction.user_id),
            category_id=transaction.category_id,
            type=transaction.type.name,
            amount=transaction.amount.value,
            occurred_at=transaction.occurred_at.isoformat(),
            description=transaction.description,
        )
