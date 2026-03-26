from app.application.dto.user_dto import CreateUserInput, UserResponse
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository


class CreateUserUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._repo = user_repo

    async def execute(self, input_data: CreateUserInput) -> UserResponse:
        if input_data.password != input_data.password_confirmation:
            raise ValueError("As senhas não conferem.")

        if await self._repo.find_by_email(input_data.email):
            raise ValueError(f"E-mail '{input_data.email}' já está em uso.")

        user = User.create(
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            email=input_data.email,
            password=input_data.password,
        )

        await self._repo.save(user)

        return UserResponse(
            user_id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )
