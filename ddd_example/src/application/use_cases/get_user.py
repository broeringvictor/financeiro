from uuid import UUID

from app.application.dtos.user_output_dto import UserOutputDTO
from app.domain.repositories.user_repository import UserRepository


class GetUserUseCase:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    def execute(self, user_id: UUID) -> UserOutputDTO:
        user = self._repo.find_by_id(user_id)
        if not user:
            raise LookupError(f"Usuário '{user_id}' não encontrado.")

        return UserOutputDTO(
            id=user.id,
            name=user.name,
            email=str(user.email),
            is_active=user.is_active,
            created_at=user.created_at,
        )
