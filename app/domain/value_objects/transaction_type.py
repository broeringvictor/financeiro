from pydantic import BaseModel, ConfigDict

from app.domain.enums.e_transaction import TransactionTypeEnum


class TransactionType(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: TransactionTypeEnum

    @classmethod
    def create(
        cls, raw: "TransactionType | TransactionTypeEnum | int | str"
    ) -> "TransactionType":
        if isinstance(raw, cls):
            return raw
        if isinstance(raw, TransactionTypeEnum):
            return cls(value=raw)
        if isinstance(raw, int):
            try:
                return cls(value=TransactionTypeEnum(raw))
            except ValueError as exc:
                raise ValueError("Input should be 1, 2 or 3") from exc
        if isinstance(raw, str):
            normalized = raw.strip()
            if not normalized:
                raise ValueError("Transaction type cannot be empty")
            if normalized.isdigit():
                return cls.create(int(normalized))
            try:
                return cls(value=TransactionTypeEnum[normalized.upper()])
            except KeyError as exc:
                raise ValueError("Input should be 1, 2 or 3") from exc
        raise ValueError("Invalid transaction type")

    @property
    def name(self) -> str:
        return self.value.name

    @property
    def number(self) -> int:
        return int(self.value.value)

    def __str__(self) -> str:
        return self.name

