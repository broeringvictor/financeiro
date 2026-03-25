from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInput:
    frist_name: str
    last_name: str
    email: str
    password: str
    password_confirmation: str


@dataclass(frozen=True)
class CreateUserOutput:
    user_id: str
    name: str
    email: str


@dataclass(frozen=True)
class UpdateUserInput:
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


@dataclass(frozen=True)
class UpdateUserOutput:
    user_id: str
    name: str
    email: str

    
    