from enum import Enum


class TransactionTypeEnum(Enum):
    """
    Enumeration representing different transaction types.
    """

    INCOME = 1
    EXPENSE = 2
    TRANSFER = 3

    def __str__(self) -> str:
        return f"TransactionTypeEnum.{self.name}"
