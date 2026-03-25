from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.user.change_password import ChangePasswordUseCase
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.get_user import GetAllUsersUseCase, GetUserUseCase
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


def get_change_password_use_case(
    session: AsyncSession = Depends(get_session),
) -> ChangePasswordUseCase:
    return ChangePasswordUseCase(user_repo=UserRepository(session))


def get_user_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetUserUseCase:
    return GetUserUseCase(user_repo=UserRepository(session))


def get_all_users_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetAllUsersUseCase:
    return GetAllUsersUseCase(user_repo=UserRepository(session))
