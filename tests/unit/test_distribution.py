"""Tests for distribution analysis."""

from hold import Hold
from analysis.distribution import DistributionReport


def make_hold():
    hold = Hold()
    hold.create_bay("A")
    hold.create_bay("B")
    hold.create_bay("C", "overflow")
    hold.move("A", "C", 300)
    hold.move("B", "C", 150)
    return hold


class TestDistributionReport:
    def test_by_bay_kind(self):
        hold = make_hold()
        report = DistributionReport(hold)
        totals = report.by_bay_kind()
        assert "standard" in totals
        assert "overflow" in totals

    def test_top_loaded(self):
        hold = make_hold()
        report = DistributionReport(hold)
        top = report.top_loaded_bays(2)
        assert len(top) == 2
        assert top[0].load >= top[1].load

    def test_empty_bays(self):
        hold = Hold()
        hold.create_bay("X")
        report = DistributionReport(hold)
        assert len(report.empty_bays()) == 1

    def test_summary(self):
        hold = make_hold()
        report = DistributionReport(hold)
        s = report.summary()
        assert s["total_bays"] == 3
        assert "total_load" in s
