from pydantic import EmailStr
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInput:
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    password_confirmation: str


@dataclass(frozen=True)
class UpdateUserBody:
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


@dataclass(frozen=True)
class UpdateUserInput:
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


@dataclass(frozen=True)
class ChangePasswordInput:
    user_id: str
    current_password: str
    new_password: str
    new_password_confirmation: str


@dataclass(frozen=True)
class UserResponse:
    user_id: str
    name: str
    email: str
