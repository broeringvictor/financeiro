from uuid import UUID

from app.application.dto.user_dto import ChangePasswordInput
from app.domain.repositories.user_repository import IUserRepository


class ChangePasswordUseCase:

    def __init__(self, user_repo: IUserRepository) -> None:
        self._repo = user_repo

    async def execute(self, input_data: ChangePasswordInput) -> None:
        if input_data.new_password != input_data.new_password_confirmation:
            raise ValueError("As novas senhas não conferem.")

        user = await self._repo.find_by_id(UUID(input_data.user_id))
        if not user:
            raise LookupError(f"Usuário '{input_data.user_id}' não encontrado.")

        user.change_password(
            current_plain=input_data.current_password,
            new_plain=input_data.new_password,
        )

        await self._repo.save(user)
