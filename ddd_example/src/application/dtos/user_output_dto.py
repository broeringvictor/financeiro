from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserOutputDTO:
    """DTO de saída — o que o caso de uso devolve para a interface."""

    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime
