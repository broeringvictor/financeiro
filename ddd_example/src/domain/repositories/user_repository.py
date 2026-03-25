from typing import Protocol, runtime_checkable
from uuid import UUID

from app.domain.entities.user import User


@runtime_checkable  # permite isinstance(repo, UserRepository) se necessário
class UserRepository(Protocol):
    """
    Contrato estrutural (Protocol) — sem herança obrigatória.

    Qualquer classe que implemente esses métodos satisfaz o contrato,
    sem precisar importar ou herdar deste módulo (duck typing estático).
    ABC força herança explícita; Protocol usa subtipagem estrutural.
    """

    def save(self, user: User) -> None: ...
    def find_by_id(self, user_id: UUID) -> User | None: ...
    def find_by_email(self, email: str) -> User | None: ...
    def list_all(self) -> list[User]: ...
