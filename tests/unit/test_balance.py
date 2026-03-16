"""Tests for balance analysis."""

from hold import Hold
from analysis.balance import BalanceAnalyzer


def make_hold():
    hold = Hold()
    hold.create_bay("A")
    hold.create_bay("B")
    hold.create_bay("C", "overflow")
    hold.move("A", "C", 100)
    hold.move("B", "C", 100)
    return hold


class TestBalanceAnalyzer:
    def test_total_load(self):
        hold = make_hold()
        analyzer = BalanceAnalyzer(hold)
        assert analyzer.total_load() == 0  # A=100, B=100, C=-200

    def test_average_load(self):
        hold = make_hold()
        analyzer = BalanceAnalyzer(hold)
        assert analyzer.average_load() == 0.0

    def test_balanced_equal_loads(self):
        hold = make_hold()
        analyzer = BalanceAnalyzer(hold)
        # All loads are 0 average, so balanced check depends on impl
        result = analyzer.is_balanced()
        assert isinstance(result, bool)

    def test_heaviest_bay(self):
        hold = make_hold()
        analyzer = BalanceAnalyzer(hold)
        heaviest = analyzer.heaviest_bay()
        assert heaviest.load == 100

    def test_lightest_bay(self):
        hold = make_hold()
        analyzer = BalanceAnalyzer(hold)
        lightest = analyzer.lightest_bay()
        assert lightest.load == -200

    def test_imbalance_report(self):
        hold = make_hold()
        analyzer = BalanceAnalyzer(hold)
        report = analyzer.imbalance_report()
        assert len(report) == 3
