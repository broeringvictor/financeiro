from uuid import UUID

from app.application.dto.user_dto import UserResponse
from app.domain.repositories.user_repository import IUserRepository


class GetUserUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._repo = user_repo

    async def execute(self, user_id: UUID) -> UserResponse:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise LookupError(f"Usuário '{user_id}' não encontrado.")

        return UserResponse(
            user_id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )


class GetAllUsersUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._repo = user_repo

    async def execute(self) -> list[UserResponse]:
        users = await self._repo.list_all()
        return [
            UserResponse(
                user_id=str(u.id),
                name=str(u.name),
                email=str(u.email),
            )
            for u in users
        ]
