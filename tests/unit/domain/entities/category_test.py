import pytest

from app.domain.entities.category import Category
from app.domain.enums.e_transaction import TransactionTypeEnum
from app.domain.value_objects.transaction_type import TransactionType


class TestCategoryCreate:
    def test_create_valid_category(self):
        category = Category.create(name="Salário", type=TransactionTypeEnum.INCOME)

        assert category.name == "Salário"
        assert category.type == TransactionType.create(TransactionTypeEnum.INCOME)
        assert category.description is None
        assert category.id is None

    def test_create_with_description(self):
        category = Category.create(
            name="Alimentação",
            type=TransactionTypeEnum.EXPENSE,
            description="Gastos com comida",
        )

        assert category.description == "Gastos com comida"

    def test_name_is_stripped(self):
        category = Category.create(name="  Aluguel  ", type=TransactionTypeEnum.EXPENSE)

        assert category.name == "Aluguel"

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Category.create(name="", type=TransactionTypeEnum.EXPENSE)

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            Category.create(name="   ", type=TransactionTypeEnum.EXPENSE)

    def test_all_transaction_types_accepted(self):
        for t in TransactionTypeEnum:
            category = Category.create(name="Categoria", type=t)
            assert category.type == TransactionType.create(t)
