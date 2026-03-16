"""Tests for Stow and StowLog classes."""

import pytest
from bay import Bay
from stow import Stow, StowLog


class TestStow:
    def test_stow_creation(self):
        a = Bay("A")
        b = Bay("B")
        stow = Stow(a, b, 100)
        assert stow.dest_bay is a
        assert stow.source_bay is b
        assert stow.weight == 100
        assert stow.note == ""

    def test_stow_with_note(self):
        a = Bay("A")
        b = Bay("B")
        stow = Stow(a, b, 50, "test note")
        assert stow.note == "test note"

    def test_stow_initial_id(self):
        a = Bay("A")
        b = Bay("B")
        stow = Stow(a, b, 100)
        assert stow.id == 0

    def test_stow_id_setter(self):
        a = Bay("A")
        b = Bay("B")
        stow = Stow(a, b, 100)
        stow.id = 5
        assert stow.id == 5


class TestStowLog:
    def test_log_empty(self):
        log = StowLog()
        assert log.stows() == []

    def test_log_record(self):
        log = StowLog()
        a = Bay("A")
        b = Bay("B")
        stow = Stow(a, b, 100)
        log.record(stow)
        assert len(log.stows()) == 1
        assert stow.id == 1

    def test_log_sequential_ids(self):
        log = StowLog()
        a = Bay("A")
        b = Bay("B")
        s1 = Stow(a, b, 100)
        s2 = Stow(b, a, 50)
        log.record(s1)
        log.record(s2)
        assert s1.id == 1
        assert s2.id == 2

    def test_log_updates_bays(self):
        log = StowLog()
        a = Bay("A")
        b = Bay("B")
        stow = Stow(a, b, 100)
        log.record(stow)
        assert len(a.stows()) == 1
        assert len(b.stows()) == 1
