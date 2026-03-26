from typing import Protocol
from uuid import UUID

from app.domain.entities.transaction import Transaction
from app.domain.value_objects.transaction_type import TransactionType


class ITransactionRepository(Protocol):
    """
    Contrato estrutural para o repositório de transações.
    A infra implementa sem precisar herdar daqui.
    """

    async def save(self, transaction: Transaction) -> None: ...
    async def find_by_id(self, transaction_id: UUID) -> Transaction | None: ...
    async def find_by_user(self, user_id: UUID) -> list[Transaction]: ...
    async def find_by_user_and_type(
        self, user_id: UUID, type: TransactionType
    ) -> list[Transaction]: ...
    async def update(self, transaction: Transaction) -> None: ...
    async def delete(self, transaction_id: UUID) -> None: ...
