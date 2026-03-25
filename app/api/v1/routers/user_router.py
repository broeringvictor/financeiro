from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_create_user_use_case
from app.api.v1.schemas.user_schema import CreateUserRequest, CreateUserResponse
from app.application.dto.user_dto import CreateUserInput
from app.application.use_cases.user.create_user import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> CreateUserResponse:
    try:
        output = await use_case.execute(
            CreateUserInput(
                frist_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
                password=body.password,
                password_confirmation=body.password_confirmation,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    return CreateUserResponse(
        user_id=output.user_id,
        name=output.name,
        email=output.email,
    )
