"""
Container de injeção de dependência.
Monta o grafo completo: session → repo → use case.
A interface (FastAPI) só faz import daqui, nunca de infra diretamente.
"""

from sqlalchemy.orm import Session

from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_user import GetUserUseCase
from app.infrastructure.database.repositories.sql_user_repo import SQLUserRepository


def get_create_user_use_case(session: Session) -> CreateUserUseCase:
    repo = SQLUserRepository(session)
    return CreateUserUseCase(user_repo=repo)


def get_get_user_use_case(session: Session) -> GetUserUseCase:
    repo = SQLUserRepository(session)
    return GetUserUseCase(user_repo=repo)
