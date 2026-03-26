from decimal import Decimal

import pytest

from app.domain.value_objects.amount import Amount


class TestAmountCreate:
    def test_create_valid_amount(self):
        amount = Amount.create(Decimal("100.00"))

        assert amount.value == Decimal("100.00")

    def test_accepts_int(self):
        amount = Amount.create(50)

        assert amount.value == Decimal("50.00")

    def test_accepts_float(self):
        amount = Amount.create(9.99)

        assert amount.value == Decimal("9.99")

    def test_accepts_string(self):
        amount = Amount.create("250.50")

        assert amount.value == Decimal("250.50")

    def test_normalizes_to_two_decimal_places(self):
        amount = Amount.create(Decimal("10.999"))

        assert amount.value == Decimal("11.00")

    def test_zero_raises(self):
        with pytest.raises(ValueError, match="maior que zero"):
            Amount.create(0)

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="maior que zero"):
            Amount.create(Decimal("-1.00"))

    def test_exceeds_max_raises(self):
        with pytest.raises(ValueError, match="valor máximo"):
            Amount.create(Decimal("1_000_000_000.00"))

    def test_invalid_string_raises(self):
        with pytest.raises(ValueError, match="Valor inválido"):
            Amount.create("abc")

    def test_max_valid_value(self):
        amount = Amount.create(Decimal("999_999_999.99"))

        assert amount.value == Decimal("999999999.99")


class TestAmountFromDecimal:
    def test_reconstructs_from_decimal(self):
        original = Amount.create(Decimal("123.45"))
        reconstructed = Amount.from_decimal(original.value)

        assert reconstructed.value == original.value

    def test_from_decimal_does_not_revalidate(self):
        # from_decimal é para leitura do banco — não aplica regras de negócio
        amount = Amount.from_decimal(Decimal("500.00"))

        assert amount.value == Decimal("500.00")


class TestAmountArithmetic:
    def test_add_two_amounts(self):
        a = Amount.create(Decimal("100.00"))
        b = Amount.create(Decimal("50.00"))

        result = a + b

        assert result.value == Decimal("150.00")

    def test_add_returns_new_instance(self):
        a = Amount.create(Decimal("100.00"))
        b = Amount.create(Decimal("50.00"))

        result = a + b

        assert result is not a
        assert result is not b

    def test_subtract_valid(self):
        a = Amount.create(Decimal("100.00"))
        b = Amount.create(Decimal("40.00"))

        result = a - b

        assert result.value == Decimal("60.00")

    def test_subtract_resulting_zero_raises(self):
        a = Amount.create(Decimal("100.00"))
        b = Amount.create(Decimal("100.00"))

        with pytest.raises(ValueError, match="inválido"):
            a - b

    def test_subtract_resulting_negative_raises(self):
        a = Amount.create(Decimal("50.00"))
        b = Amount.create(Decimal("100.00"))

        with pytest.raises(ValueError, match="inválido"):
            a - b


class TestAmountImmutability:
    def test_cannot_overwrite_value(self):
        amount = Amount.create(Decimal("100.00"))

        with pytest.raises(Exception):
            amount.value = Decimal("999.00")  # type: ignore[misc]


class TestAmountStr:
    def test_str_returns_decimal_string(self):
        amount = Amount.create(Decimal("42.50"))

        assert str(amount) == "42.50"
