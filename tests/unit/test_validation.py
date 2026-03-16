"""Tests for validation utilities."""

import pytest
from utils.validation import (
    validate_bay_name,
    validate_weight,
    validate_bay_kind,
    validate_stow_data,
)


class TestValidateBayName:
    def test_valid_name(self):
        valid, msg = validate_bay_name("FORE-1")
        assert valid is True

    def test_empty_name(self):
        valid, msg = validate_bay_name("")
        assert valid is False

    def test_non_string(self):
        valid, msg = validate_bay_name(123)
        assert valid is False

    def test_lowercase_invalid(self):
        valid, msg = validate_bay_name("fore-1")
        assert valid is False


class TestValidateWeight:
    def test_valid_weight(self):
        valid, msg = validate_weight(100)
        assert valid is True

    def test_zero_weight(self):
        valid, msg = validate_weight(0)
        assert valid is False

    def test_negative_weight(self):
        valid, msg = validate_weight(-10)
        assert valid is False

    def test_non_numeric(self):
        valid, msg = validate_weight("heavy")
        assert valid is False


class TestValidateBayKind:
    def test_standard(self):
        valid, msg = validate_bay_kind("standard")
        assert valid is True

    def test_overflow(self):
        valid, msg = validate_bay_kind("overflow")
        assert valid is True

    def test_invalid_kind(self):
        valid, msg = validate_bay_kind("magic")
        assert valid is False
