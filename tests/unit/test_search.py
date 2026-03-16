"""Tests for search utilities."""

from hold import Hold
from utils.search import (
    find_stows_by_note,
    find_bays_by_kind,
    find_empty_bays,
    find_heaviest_stow,
    count_stows_per_bay,
)


def make_hold():
    hold = Hold()
    hold.create_bay("A")
    hold.create_bay("B")
    hold.create_bay("C", "overflow")
    hold.move("A", "C", 100, "load")
    hold.move("B", "C", 200, "load")
    hold.move("A", "B", 50, "transfer")
    return hold


class TestFindStowsByNote:
    def test_find_by_note(self):
        hold = make_hold()
        results = find_stows_by_note(hold, "load")
        assert len(results) == 2

    def test_find_no_match(self):
        hold = make_hold()
        results = find_stows_by_note(hold, "xyz")
        assert len(results) == 0


class TestFindBaysByKind:
    def test_find_standard(self):
        hold = make_hold()
        results = find_bays_by_kind(hold, "standard")
        assert len(results) == 2

    def test_find_overflow(self):
        hold = make_hold()
        results = find_bays_by_kind(hold, "overflow")
        assert len(results) == 1


class TestFindEmptyBays:
    def test_no_empty(self):
        hold = make_hold()
        results = find_empty_bays(hold)
        assert len(results) == 0


class TestFindHeaviestStow:
    def test_heaviest(self):
        hold = make_hold()
        stow = find_heaviest_stow(hold)
        assert stow.weight == 200


class TestCountStowsPerBay:
    def test_counts(self):
        hold = make_hold()
        counts = count_stows_per_bay(hold)
        assert counts["C"] == 2
