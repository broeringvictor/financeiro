from uuid import UUID

from app.application.dto.user_dto import UpdateUserInput, UpdateUserOutput
from app.domain.repositories.user_repository import IUserRepository


class UpdateUserUseCase:

    def __init__(self, user_repo: IUserRepository) -> None:
        self._repo = user_repo

    async def execute(self, input_data: UpdateUserInput) -> UpdateUserOutput:
        user = await self._repo.find_by_id(UUID(input_data.user_id))
        if not user:
            raise LookupError(f"Usuário '{input_data.user_id}' não encontrado.")

        if input_data.email and input_data.email != str(user.email):
            if await self._repo.find_by_email(input_data.email):
                raise ValueError(f"E-mail '{input_data.email}' já está em uso.")

        # usa o método da entidade — regras de negócio ficam no domínio
        user.update(
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            email=input_data.email,
        )

        await self._repo.save(user)

        return UpdateUserOutput(
            user_id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )
