"""FastAPI Depends — cola entre o framework e o container DI."""

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_user import GetUserUseCase
from app.container import get_create_user_use_case, get_get_user_use_case
from app.infrastructure.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield de sessão com garantia de fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user_use_case(
    session: Session = Depends(get_db),
) -> CreateUserUseCase:
    return get_create_user_use_case(session)


def get_user_use_case(
    session: Session = Depends(get_db),
) -> GetUserUseCase:
    return get_get_user_use_case(session)
