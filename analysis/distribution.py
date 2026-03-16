"""Distribution analysis and reporting for cargo holds."""


class DistributionReport:
    """Generates reports on cargo weight distribution."""

    def __init__(self, hold):
        self._hold = hold

    def by_bay_kind(self):
        """Group total loads by bay kind."""
        totals = {}
        for bay in self._hold.bays():
            kind = bay.kind
            if kind not in totals:
                totals[kind] = 0
            totals[kind] += bay.load
        return totals

    def load_histogram(self, bin_size=100):
        """Create a histogram of bay loads."""
        bins = {}
        for bay in self._hold.bays():
            load = bay.load
            bin_key = (load // bin_size) * bin_size
            label = f"{bin_key}-{bin_key + bin_size - 1}"
            if label not in bins:
                bins[label] = 0
            bins[label] += 1
        return bins

    def percentile_rank(self, bay_name):
        """Calculate the percentile rank of a bay's load."""
        target = self._hold.get_bay(bay_name)
        loads = sorted(bay.load for bay in self._hold.bays())
        if not loads:
            return 0.0
        rank = sum(1 for l in loads if l <= target.load)
        return (rank / len(loads)) * 100

    def top_loaded_bays(self, n=5):
        """Return the top N loaded bays."""
        bays = sorted(self._hold.bays(), key=lambda b: b.load, reverse=True)
        return bays[:n]

    def bottom_loaded_bays(self, n=5):
        """Return the bottom N loaded bays."""
        bays = sorted(self._hold.bays(), key=lambda b: b.load)
        return bays[:n]

    def empty_bays(self):
        """Return bays with zero load."""
        return [bay for bay in self._hold.bays() if bay.load == 0]

    def non_empty_bays(self):
        """Return bays with non-zero load."""
        return [bay for bay in self._hold.bays() if bay.load != 0]

    def utilization_rate(self, max_capacity=10000):
        """Calculate the utilization rate of the hold."""
        total_capacity = max_capacity * len(self._hold.bays())
        if total_capacity == 0:
            return 0.0
        total_load = sum(bay.load for bay in self._hold.bays())
        return total_load / total_capacity

    def summary(self):
        """Generate a summary dictionary of the distribution."""
        bays = self._hold.bays()
        loads = [bay.load for bay in bays]
        if not loads:
            return {
                "total_bays": 0,
                "total_load": 0,
                "min_load": 0,
                "max_load": 0,
                "avg_load": 0,
                "empty_count": 0,
            }
        return {
            "total_bays": len(bays),
            "total_load": sum(loads),
            "min_load": min(loads),
            "max_load": max(loads),
            "avg_load": round(sum(loads) / len(loads), 2),
            "empty_count": sum(1 for l in loads if l == 0),
        }
