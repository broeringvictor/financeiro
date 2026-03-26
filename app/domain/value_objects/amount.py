from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, ConfigDict


class Amount(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Decimal

    @classmethod
    def create(cls, value: Decimal | int | float | str) -> "Amount":
        """Valida e retorna um Amount com o valor normalizado."""
        try:
            amount = Decimal(str(value))
        except InvalidOperation:
            raise ValueError(f"Valor inválido para Amount: '{value}'.")

        if amount <= 0:
            raise ValueError("Amount deve ser maior que zero.")
        if amount > Decimal("999_999_999.99"):
            raise ValueError("Amount excede o valor máximo permitido.")

        return cls(value=amount.quantize(Decimal("0.01")))

    @classmethod
    def from_decimal(cls, value: Decimal) -> "Amount":
        """Reconstrói o VO a partir de um valor já validado (ex: leitura do banco)."""
        return cls(value=value)

    def __add__(self, other: "Amount") -> "Amount":
        return Amount(value=self.value + other.value)

    def __sub__(self, other: "Amount") -> "Amount":
        result = self.value - other.value
        if result <= 0:
            raise ValueError("Subtração resultaria em Amount inválido.")
        return Amount(value=result)

    def __str__(self) -> str:
        return str(self.value)
