from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from app.domain.value_objects.email import Email
from app.domain.events.user_created_event import UserCreatedEvent


class User(BaseModel):
    """
    Entidade com Pydantic — mais Pythônico que dataclass para este caso.

    Por que Pydantic em vez de dataclass:
    - PrivateAttr → _events sem o campo extra field(compare=False, repr=False)
    - field_validator → validação declarativa, sem __post_init__ manual
    - arbitrary_types_allowed → aceita o VO Email sem conversão

    Cuidado obrigatório: Pydantic compara por VALOR por padrão.
    Entidades têm identidade por ID → __eq__ e __hash__ sobrescritos.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(default_factory=uuid4)
    name: str
    email: Email
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    _events: list = PrivateAttr(default_factory=list)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome deve ter ao menos 2 caracteres.")
        return v

    # ── identidade de entidade (por ID, não por valor) ────────────────────────

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    # ── factory method ────────────────────────────────────────────────────────

    @classmethod
    def create(cls, name: str, raw_email: str) -> "User":
        """Único ponto de criação válido — garante o evento de domínio."""
        user = cls(name=name, email=Email(value=raw_email))
        user._events.append(UserCreatedEvent(user_id=user.id, email=raw_email))
        return user

    # ── comportamentos ────────────────────────────────────────────────────────

    def deactivate(self) -> None:
        if not self.is_active:
            raise ValueError("Usuário já está inativo.")
        self.is_active = False

    def collect_events(self) -> list:
        events, self._events = self._events, []
        return events
