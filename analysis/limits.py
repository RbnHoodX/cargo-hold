"""Load limit checking and safety validation."""

from config import MAX_BAY_LOAD, OVERLOAD_WARNING_RATIO, CRITICAL_LOAD_RATIO


class LimitChecker:
    """Checks load limits and safety constraints for a hold."""

    def __init__(self, hold, max_load=None):
        self._hold = hold
        self._max_load = max_load or MAX_BAY_LOAD

    @property
    def max_load(self):
        return self._max_load

    def check_bay(self, bay_name):
        """Check a single bay against limits.

        Returns:
            A dict with status ('ok', 'warning', 'critical', 'overloaded')
            and details.
        """
        bay = self._hold.get_bay(bay_name)
        load = bay.load
        ratio = load / self._max_load if self._max_load > 0 else 0

        if load > self._max_load:
            status = "overloaded"
        elif ratio >= CRITICAL_LOAD_RATIO:
            status = "critical"
        elif ratio >= OVERLOAD_WARNING_RATIO:
            status = "warning"
        else:
            status = "ok"

        return {
            "bay": bay_name,
            "load": load,
            "max_load": self._max_load,
            "ratio": round(ratio, 4),
            "status": status,
        }

    def check_all(self):
        """Check all bays against limits."""
        results = []
        for bay in self._hold.bays():
            results.append(self.check_bay(bay.name))
        return results

    def overloaded_bays(self):
        """Return list of overloaded bays."""
        return [r for r in self.check_all() if r["status"] == "overloaded"]

    def warning_bays(self):
        """Return bays at warning or above."""
        return [r for r in self.check_all()
                if r["status"] in ("warning", "critical", "overloaded")]

    def is_safe(self):
        """Check if all bays are within safe limits."""
        return len(self.overloaded_bays()) == 0

    def remaining_capacity(self, bay_name):
        """Calculate remaining capacity for a bay."""
        bay = self._hold.get_bay(bay_name)
        return max(0, self._max_load - bay.load)

    def total_remaining_capacity(self):
        """Calculate total remaining capacity across all bays."""
        return sum(
            self.remaining_capacity(bay.name) for bay in self._hold.bays()
        )

    def can_accept(self, bay_name, weight):
        """Check if a bay can accept additional weight."""
        return self.remaining_capacity(bay_name) >= weight

    def suggest_bay(self, weight):
        """Suggest the best bay for a given weight.

        Returns the bay with the most remaining capacity that can accept
        the weight, or None if no bay can.
        """
        candidates = []
        for bay in self._hold.bays():
            remaining = self.remaining_capacity(bay.name)
            if remaining >= weight:
                candidates.append((bay, remaining))
        if not candidates:
            return None
        candidates.sort(key=lambda c: c[1], reverse=True)
        return candidates[0][0]
