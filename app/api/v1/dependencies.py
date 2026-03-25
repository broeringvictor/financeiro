from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.infra.repositories.user_repository import UserRepository
from app.infra.session import get_session


def get_create_user_use_case(
    session: AsyncSession = Depends(get_session),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo=UserRepository(session))


def get_update_user_use_case(
    session: AsyncSession = Depends(get_session),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(user_repo=UserRepository(session))
