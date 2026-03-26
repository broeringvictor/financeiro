from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.category.create_category import CreateCategoryUseCase
from app.application.use_cases.category.delete_category import DeleteCategoryUseCase
from app.application.use_cases.category.get_all_categories import GetAllCategoriesUseCase as GetAllCategoriesUseCase
from app.application.use_cases.category.get_category import GetCategoriesByTypeUseCase, GetCategoryUseCase
from app.application.use_cases.category.update_category import UpdateCategoryUseCase
from app.application.use_cases.transaction.create_transaction import CreateTransactionUseCase
from app.application.use_cases.transaction.delete_transaction import DeleteTransactionUseCase
from app.application.use_cases.transaction.get_all_transactions import GetUserTransactionsByTypeUseCase, GetUserTransactionsUseCase
from app.application.use_cases.transaction.get_transaction import GetTransactionUseCase
from app.application.use_cases.transaction.update_transaction import UpdateTransactionUseCase
from app.application.use_cases.user.change_password import ChangePasswordUseCase
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.get_user import GetAllUsersUseCase, GetUserUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.infra.repositories.category_repository import CategoryRepository
from app.infra.repositories.transaction_repository import TransactionRepository
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


# ── Category ──────────────────────────────────────────────────────────────────

def get_create_category_use_case(
    session: AsyncSession = Depends(get_session),
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(repo=CategoryRepository(session))


def get_update_category_use_case(
    session: AsyncSession = Depends(get_session),
) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(repo=CategoryRepository(session))


def get_delete_category_use_case(
    session: AsyncSession = Depends(get_session),
) -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase(repo=CategoryRepository(session))


def get_category_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetCategoryUseCase:
    return GetCategoryUseCase(repo=CategoryRepository(session))


def get_all_categories_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase(repo=CategoryRepository(session))


def get_categories_by_type_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetCategoriesByTypeUseCase:
    return GetCategoriesByTypeUseCase(repo=CategoryRepository(session))


# ── Transaction ───────────────────────────────────────────────────────────────

def get_create_transaction_use_case(
    session: AsyncSession = Depends(get_session),
) -> CreateTransactionUseCase:
    return CreateTransactionUseCase(
        transaction_repo=TransactionRepository(session),
        user_repo=UserRepository(session),
    )


def get_update_transaction_use_case(
    session: AsyncSession = Depends(get_session),
) -> UpdateTransactionUseCase:
    return UpdateTransactionUseCase(repo=TransactionRepository(session))


def get_delete_transaction_use_case(
    session: AsyncSession = Depends(get_session),
) -> DeleteTransactionUseCase:
    return DeleteTransactionUseCase(repo=TransactionRepository(session))


def get_transaction_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetTransactionUseCase:
    return GetTransactionUseCase(repo=TransactionRepository(session))


def get_user_transactions_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetUserTransactionsUseCase:
    return GetUserTransactionsUseCase(repo=TransactionRepository(session))


def get_user_transactions_by_type_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetUserTransactionsByTypeUseCase:
    return GetUserTransactionsByTypeUseCase(repo=TransactionRepository(session))
