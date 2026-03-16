"""Tests for the Bay class."""

import pytest
from bay import Bay


class TestBayCreation:
    def test_create_bay_with_name(self):
        bay = Bay("FORE-1")
        assert bay.name == "FORE-1"

    def test_create_bay_default_kind(self):
        bay = Bay("FORE-1")
        assert bay.kind == "standard"

    def test_create_bay_custom_kind(self):
        bay = Bay("AFT-1", kind="overflow")
        assert bay.kind == "overflow"

    def test_bay_initial_load_zero(self):
        bay = Bay("MID-1")
        assert bay.load == 0

    def test_bay_initial_stows_empty(self):
        bay = Bay("MID-1")
        assert bay.stows() == []


class TestBayRepr:
    def test_repr_standard(self):
        bay = Bay("FORE-1")
        assert repr(bay) == "Bay(name='FORE-1', kind='standard')"

    def test_repr_overflow(self):
        bay = Bay("AFT-2", "overflow")
        assert repr(bay) == "Bay(name='AFT-2', kind='overflow')"
