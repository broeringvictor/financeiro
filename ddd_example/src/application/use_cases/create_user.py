from app.application.dtos.user_input_dto import CreateUserInputDTO
from app.application.dtos.user_output_dto import UserOutputDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    """
    Orquestra a criação de um usuário.
    Conhece repositórios e entidades, mas não sabe nada de HTTP ou banco.
    """

    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    def execute(self, dto: CreateUserInputDTO) -> UserOutputDTO:
        # Regra de negócio: e-mail único
        if self._repo.find_by_email(dto.email):
            raise ValueError(f"E-mail '{dto.email}' já está em uso.")

        user = User.create(name=dto.name, raw_email=dto.email)
        self._repo.save(user)

        # Aqui você poderia despachar os eventos acumulados
        # event_bus.publish(user.collect_events())

        return UserOutputDTO(
            id=user.id,
            name=user.name,
            email=str(user.email),
            is_active=user.is_active,
            created_at=user.created_at,
        )
