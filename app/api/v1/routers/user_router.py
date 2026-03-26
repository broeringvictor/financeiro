from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.api.exception_handlers import format_errors
from app.api.v1.dependencies import (
    get_all_users_use_case,
    get_change_password_use_case,
    get_create_user_use_case,
    get_update_user_use_case,
    get_user_use_case,
)
from app.application.dto.user_dto import (
    ChangePasswordInput,
    CreateUserInput,
    UpdateUserInput,
    UserResponse,
)
from app.application.use_cases.user.change_password import ChangePasswordUseCase
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.get_user import GetAllUsersUseCase, GetUserUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])


def _handle_exc(exc: Exception) -> None:
    if isinstance(exc, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=format_errors(exc.errors()),
        )
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserInput,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(body)
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    use_case: GetAllUsersUseCase = Depends(get_all_users_use_case),
) -> list[UserResponse]:
    return await use_case.execute()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    use_case: GetUserUseCase = Depends(get_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    body: UpdateUserInput,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(
            UpdateUserInput(
                user_id=user_id,
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
            )
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)


@router.patch("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_id: str,
    body: ChangePasswordInput,
    use_case: ChangePasswordUseCase = Depends(get_change_password_use_case),
) -> None:
    try:
        await use_case.execute(
            ChangePasswordInput(
                user_id=user_id,
                current_password=body.current_password,
                new_password=body.new_password,
                new_password_confirmation=body.new_password_confirmation,
            )
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (ValidationError, ValueError) as exc:
        _handle_exc(exc)
