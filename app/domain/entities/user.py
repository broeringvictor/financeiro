from datetime import UTC, datetime
from uuid import uuid8

from pydantic import UUID8, BaseModel, EmailStr, Field, StrictBool, field_validator

from app.domain.entities.transaction import Transaction
from app.domain.value_objects.name import Name
from app.domain.value_objects.password import Password


class User(BaseModel):
    id: UUID8 = Field(default_factory=uuid8)
    name: Name
    email: EmailStr
    password: Password
    is_active: StrictBool
    create_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    modified_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    transactions: list[Transaction] = Field(default_factory=list)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        password: str,
        email: str,
    ) -> "User":
        """Único ponto de criação válido."""
        return cls(
            name=Name(first_name=first_name, last_name=last_name),
            password=Password.create(password),
            email=email,
            is_active=True,
        )

    def change_password(self, current_plain: str, new_plain: str) -> None:
        """Troca a senha após verificar a senha atual."""
        if not self.password.verify(current_plain):
            raise ValueError("Senha atual incorreta.")
        self.password = Password.create(new_plain)
        self.modified_at = datetime.now(UTC)

    def update(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> None:
        """Edita os dados do usuário. Apenas os campos informados são alterados."""
        if first_name is not None or last_name is not None:
            self.name = Name(
                first_name=first_name
                if first_name is not None
                else self.name.first_name,
                last_name=last_name if last_name is not None else self.name.last_name,
            )
        if email is not None:
            self.email = email
        self.modified_at = datetime.now(UTC)

    def public_user(self) -> dict:
        return self.model_dump(exclude={"password"})
