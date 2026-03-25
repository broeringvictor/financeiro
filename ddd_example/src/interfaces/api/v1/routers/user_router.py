from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.user_input_dto import CreateUserInputDTO
from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_user import GetUserUseCase
from app.interfaces.api.dependencies import create_user_use_case, get_user_use_case
from app.interfaces.api.v1.schemas.user_schema import CreateUserRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> UserResponse:
    """
    Rota HTTP → converte schema para DTO → chama use case → converte DTO para response.
    Sem lógica de negócio aqui.
    """
    try:
        output = use_case.execute(
            CreateUserInputDTO(name=body.name, email=body.email)
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    return UserResponse(
        id=output.id,
        name=output.name,
        email=output.email,
        is_active=output.is_active,
        created_at=output.created_at,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    use_case: GetUserUseCase = Depends(get_user_use_case),
) -> UserResponse:
    try:
        output = use_case.execute(user_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return UserResponse(
        id=output.id,
        name=output.name,
        email=output.email,
        is_active=output.is_active,
        created_at=output.created_at,
    )


@router.get("/", response_model=list[UserResponse])
def list_users(
    use_case: GetUserUseCase = Depends(get_user_use_case),
) -> list[UserResponse]:
    # Reutiliza o repo diretamente via use case seria o ideal,
    # mas para o exemplo simplificamos aqui.
    repo = use_case._repo  # em produção: crie um ListUsersUseCase dedicado
    users = repo.list_all()
    return [
        UserResponse(
            id=u.id,
            name=u.name,
            email=str(u.email),
            is_active=u.is_active,
            created_at=u.created_at,
        )
        for u in users
    ]
