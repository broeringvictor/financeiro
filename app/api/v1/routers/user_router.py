from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.api.exception_handlers import format_errors
from app.api.v1.dependencies import get_create_user_use_case
from app.application.dto.user_dto import CreateUserInput, UserResponse
from app.application.use_cases.user.create_user import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserInput,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(body)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=format_errors(exc.errors()))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
