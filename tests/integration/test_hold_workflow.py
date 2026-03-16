"""Integration tests for hold workflows."""

import pytest
from hold import Hold


class TestHoldWorkflow:
    def test_create_load_check(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 500)
        assert hold.get_bay("A").load == 500
        assert hold.get_bay("B").load == -500

    def test_multiple_moves(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B")
        hold.create_bay("C", "overflow")
        hold.move("A", "C", 100)
        hold.move("B", "C", 200)
        hold.move("B", "A", 50)
        assert hold.get_bay("A").load == 50
        assert hold.get_bay("B").load == 250
        assert hold.get_bay("C").load == -300

    def test_log_ordering(self):
        hold = Hold()
        hold.create_bay("X")
        hold.create_bay("Y", "overflow")
        hold.move("X", "Y", 10)
        hold.move("X", "Y", 20)
        hold.move("X", "Y", 30)
        entries = hold.log_entries()
        assert [e.id for e in entries] == [1, 2, 3]
        assert [e.weight for e in entries] == [10, 20, 30]

    def test_weight_summary_consistency(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 100)
        hold.move("B", "A", 30)
        total_in, total_out = hold.weight_summary()
        assert total_in == 130
        assert total_out == 130
