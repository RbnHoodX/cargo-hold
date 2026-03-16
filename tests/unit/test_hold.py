"""Tests for the Hold class."""

import pytest
from hold import Hold


class TestHoldCreation:
    def test_create_hold(self):
        hold = Hold()
        assert hold.bays() == []

    def test_create_bay(self):
        hold = Hold()
        bay = hold.create_bay("A")
        assert bay.name == "A"
        assert bay.kind == "standard"

    def test_create_bay_custom_kind(self):
        hold = Hold()
        bay = hold.create_bay("A", "overflow")
        assert bay.kind == "overflow"

    def test_create_duplicate_bay_raises(self):
        hold = Hold()
        hold.create_bay("A")
        with pytest.raises(ValueError):
            hold.create_bay("A")

    def test_get_bay(self):
        hold = Hold()
        hold.create_bay("A")
        bay = hold.get_bay("A")
        assert bay.name == "A"

    def test_get_bay_missing_raises(self):
        hold = Hold()
        with pytest.raises(KeyError):
            hold.get_bay("X")


class TestHoldMove:
    def test_move_basic(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 100)
        assert hold.get_bay("A").load == 100
        assert hold.get_bay("B").load == -100

    def test_move_with_note(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        stow = hold.move("A", "B", 50, "test")
        assert stow.note == "test"

    def test_move_zero_raises(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B")
        with pytest.raises(ValueError):
            hold.move("A", "B", 0)

    def test_move_negative_raises(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B")
        with pytest.raises(ValueError):
            hold.move("A", "B", -10)


class TestHoldLog:
    def test_log_entries_empty(self):
        hold = Hold()
        assert hold.log_entries() == []

    def test_log_entries_after_move(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 100)
        entries = hold.log_entries()
        assert len(entries) == 1
        assert entries[0].weight == 100


class TestWeightSummary:
    def test_summary_empty(self):
        hold = Hold()
        assert hold.weight_summary() == (0, 0)

    def test_summary_after_moves(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 100)
        hold.move("A", "B", 200)
        total_in, total_out = hold.weight_summary()
        assert total_in == 300
        assert total_out == 300
