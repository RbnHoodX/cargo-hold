"""Balance analysis for cargo distribution across bays."""

from config import BALANCE_TOLERANCE


class BalanceAnalyzer:
    """Analyzes weight distribution balance across a hold."""

    def __init__(self, hold):
        self._hold = hold

    def total_load(self):
        """Calculate total load across all bays."""
        return sum(bay.load for bay in self._hold.bays())

    def average_load(self):
        """Calculate average load per bay."""
        bays = self._hold.bays()
        if not bays:
            return 0
        return self.total_load() / len(bays)

    def load_variance(self):
        """Calculate variance in load distribution."""
        bays = self._hold.bays()
        if not bays:
            return 0
        avg = self.average_load()
        return sum((bay.load - avg) ** 2 for bay in bays) / len(bays)

    def load_std_dev(self):
        """Calculate standard deviation of load distribution."""
        return self.load_variance() ** 0.5

    def is_balanced(self, tolerance=None):
        """Check if load is balanced within tolerance.

        Balance means no bay deviates from the average by more than
        tolerance percent of the average.
        """
        if tolerance is None:
            tolerance = BALANCE_TOLERANCE
        avg = self.average_load()
        if avg == 0:
            return True
        for bay in self._hold.bays():
            deviation = abs(bay.load - avg) / avg
            if deviation > tolerance:
                return False
        return True

    def heaviest_bay(self):
        """Return the bay with the most load."""
        bays = self._hold.bays()
        if not bays:
            return None
        return max(bays, key=lambda b: b.load)

    def lightest_bay(self):
        """Return the bay with the least load."""
        bays = self._hold.bays()
        if not bays:
            return None
        return min(bays, key=lambda b: b.load)

    def imbalance_report(self):
        """Generate a report of load imbalances."""
        avg = self.average_load()
        report = []
        for bay in self._hold.bays():
            diff = bay.load - avg
            pct = (diff / avg * 100) if avg != 0 else 0
            report.append({
                "bay": bay.name,
                "load": bay.load,
                "deviation": round(diff, 2),
                "deviation_pct": round(pct, 2),
            })
        report.sort(key=lambda r: abs(r["deviation"]), reverse=True)
        return report

    def fore_aft_ratio(self):
        """Calculate the fore-to-aft load ratio."""
        bays = self._hold.bays()
        if not bays:
            return 1.0
        mid = len(bays) // 2
        fore_load = sum(b.load for b in bays[:mid]) or 1
        aft_load = sum(b.load for b in bays[mid:]) or 1
        return fore_load / aft_load
