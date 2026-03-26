from uuid import UUID

from app.application.dto.user_dto import UpdateUserInput, UserResponse
from app.domain.repositories.user_repository import IUserRepository


class UpdateUserUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._repo = user_repo

    async def execute(self, input_data: UpdateUserInput) -> UserResponse:
        user = await self._repo.find_by_id(UUID(input_data.user_id))
        if not user:
            raise LookupError(f"Usuário '{input_data.user_id}' não encontrado.")

        if input_data.email and input_data.email != str(user.email):
            if await self._repo.find_by_email(input_data.email):
                raise ValueError(f"E-mail '{input_data.email}' já está em uso.")

        user.update(
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            email=input_data.email,
        )

        await self._repo.save(user)

        return UserResponse(
            user_id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )
