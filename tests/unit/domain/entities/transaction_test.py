from decimal import Decimal
from uuid import uuid8

import pytest

from app.domain.entities.transaction import Transaction
from app.domain.enums.e_transaction import TransactionType


class TestTransactionCreate:
    def test_create_valid_transaction(self):
        user_id = uuid8()
        transaction = Transaction.create(
            user_id=user_id,
            category_id=1,
            type=TransactionType.INCOME,
            amount=Decimal("100.00"),
        )

        assert transaction.user_id == user_id
        assert transaction.category_id == 1
        assert transaction.type == TransactionType.INCOME
        assert transaction.amount.value == Decimal("100.00")
        assert transaction.description is None
        assert transaction.id is not None
        assert transaction.occurred_at is not None

    def test_create_with_description(self):
        transaction = Transaction.create(
            user_id=uuid8(),
            category_id=1,
            type=TransactionType.EXPENSE,
            amount=Decimal("50.00"),
            description="Conta de luz",
        )

        assert transaction.description == "Conta de luz"

    def test_each_transaction_has_unique_id(self):
        user_id = uuid8()
        t1 = Transaction.create(user_id=user_id, category_id=1, type=TransactionType.INCOME, amount=Decimal("10"))
        t2 = Transaction.create(user_id=user_id, category_id=1, type=TransactionType.INCOME, amount=Decimal("10"))

        assert t1.id != t2.id

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError, match="maior que zero"):
            Transaction.create(
                user_id=uuid8(),
                category_id=1,
                type=TransactionType.EXPENSE,
                amount=Decimal("0"),
            )

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="maior que zero"):
            Transaction.create(
                user_id=uuid8(),
                category_id=1,
                type=TransactionType.EXPENSE,
                amount=Decimal("-10.00"),
            )

    def test_all_transaction_types_accepted(self):
        for t in TransactionType:
            transaction = Transaction.create(
                user_id=uuid8(),
                category_id=1,
                type=t,
                amount=Decimal("1.00"),
            )
            assert transaction.type == t
