import pytest
from utils.exchange import flag, DEFAULT_CURRENCIES, CURRENCY_FLAG


class TestFlag:
    """Test flag emoji function."""

    def test_known_currencies(self):
        assert flag("USD") == "🇺🇸"
        assert flag("EUR") == "🇪🇺"
        assert flag("VND") == "🇻🇳"
        assert flag("JPY") == "🇯🇵"

    def test_case_insensitive(self):
        assert flag("usd") == "🇺🇸"
        assert flag("Eur") == "🇪🇺"

    def test_unknown_currency(self):
        assert flag("XYZ") == "💱"
        assert flag("ABC") == "💱"


class TestDefaultCurrencies:
    """Test DEFAULT_CURRENCIES list."""

    def test_is_list(self):
        assert isinstance(DEFAULT_CURRENCIES, list)

    def test_contains_major_currencies(self):
        assert "USD" in DEFAULT_CURRENCIES
        assert "EUR" in DEFAULT_CURRENCIES
        assert "JPY" in DEFAULT_CURRENCIES

    def test_all_uppercase(self):
        for cur in DEFAULT_CURRENCIES:
            assert cur == cur.upper(), f"{cur} is not uppercase"

    def test_all_have_flags(self):
        for cur in DEFAULT_CURRENCIES:
            assert cur in CURRENCY_FLAG, f"{cur} missing flag emoji"
