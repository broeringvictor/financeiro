from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    """Schema Pydantic — validação HTTP de entrada (camada de interface)."""

    name: str
    email: EmailStr


class UserResponse(BaseModel):
    """Schema de saída — serialização HTTP."""

    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
