from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserCreatedEvent:
    """Evento de domínio — algo que aconteceu e é imutável."""

    user_id: UUID
    email: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)
