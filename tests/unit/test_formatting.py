"""Tests for formatting utilities."""

from bay import Bay
from utils.formatting import (
    format_weight,
    format_bay_status,
    format_header,
    truncate,
)


class TestFormatWeight:
    def test_integer_weight(self):
        assert format_weight(100) == "100 tons"

    def test_float_weight(self):
        result = format_weight(100.5)
        assert "100.50" in result

    def test_custom_unit(self):
        assert format_weight(50, unit="kg") == "50 kg"


class TestFormatBayStatus:
    def test_standard_bay(self):
        bay = Bay("FORE-1")
        result = format_bay_status(bay)
        assert "FORE-1" in result
        assert "0 tons" in result

    def test_overflow_bay(self):
        bay = Bay("AFT-2", "overflow")
        result = format_bay_status(bay)
        assert "[overflow]" in result


class TestFormatHeader:
    def test_header(self):
        result = format_header("TEST")
        assert "TEST" in result
        assert "=" in result


class TestTruncate:
    def test_short_text(self):
        assert truncate("hello", 10) == "hello"

    def test_long_text(self):
        result = truncate("a" * 60, 50)
        assert len(result) == 50
        assert result.endswith("...")
