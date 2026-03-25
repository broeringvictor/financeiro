import re

from pydantic import BaseModel, ConfigDict, field_validator


class Email(BaseModel):
    """
    Value Object com Pydantic.

    Vantagem sobre dataclass(frozen=True):
    - field_validator substitui o hack object.__setattr__ em __post_init__
    - frozen=True via ConfigDict, sem decorador separado
    - Validação e normalização declarativas
    """

    model_config = ConfigDict(frozen=True)

    value: str

    _PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", re.IGNORECASE)

    @field_validator("value", mode="before")
    @classmethod
    def normalize_and_validate(cls, v: str) -> str:
        v = v.lower().strip()
        if not cls._PATTERN.match(v):
            raise ValueError(f"E-mail inválido: '{v}'")
        return v

    def __str__(self) -> str:
        return self.value
