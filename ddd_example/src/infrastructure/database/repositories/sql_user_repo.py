from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.infrastructure.database.models.user_model import UserModel


class SQLUserRepository:
    """
    Implementa UserRepository via subtipagem estrutural (Protocol).

    Não herda de UserRepository — o type checker verifica a compatibilidade
    pelos métodos, não pela herança. A anotação de tipo no container
    e no use case é suficiente para garantir o contrato.

    Se quiser sinalizar intenção explicitamente, basta anotar:
        repo: UserRepository = SQLUserRepository(session)
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    # ── persistência ──────────────────────────────────────────────────────────

    def save(self, user: User) -> None:
        model = self._to_model(user)
        self._session.merge(model)
        self._session.commit()

    # ── consultas ─────────────────────────────────────────────────────────────

    def find_by_id(self, user_id: UUID) -> User | None:
        model = self._session.get(UserModel, str(user_id))
        return self._to_entity(model) if model else None

    def find_by_email(self, email: str) -> User | None:
        model = (
            self._session.query(UserModel)
            .filter_by(email=email.lower().strip())
            .first()
        )
        return self._to_entity(model) if model else None

    def list_all(self) -> list[User]:
        return [self._to_entity(m) for m in self._session.query(UserModel).all()]

    # ── mapeamento (anti-corruption layer interno) ────────────────────────────

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            id=str(user.id),
            name=user.name,
            email=str(user.email),
            is_active=user.is_active,
            created_at=user.created_at,
        )

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        # Reconstrói a entidade do banco sem passar pelo factory method
        # (eventos não são reemitidos na reconstrução — comportamento correto)
        return User(
            id=UUID(model.id),
            name=model.name,
            email=Email(value=model.email),   # Email(value=...) com Pydantic
            is_active=model.is_active,
            created_at=model.created_at,
        )
