from bay import Bay
from stow import Stow, StowLog


class Hold:
    """Cargo hold managing bays and cargo stow operations."""

    def __init__(self):
        self._bays = {}
        self._log = StowLog()

    def create_bay(self, name, kind="standard"):
        if name in self._bays:
            raise ValueError(f"bay {name!r} already exists")
        bay = Bay(name, kind)
        self._bays[name] = bay
        return bay

    def get_bay(self, name):
        return self._bays[name]

    def bays(self):
        return list(self._bays.values())

    def move(self, dest_name, source_name, weight, note=""):
        if weight <= 0:
            raise ValueError("weight must be positive")
        dest_bay = self._bays[dest_name]
        source_bay = self._bays[source_name]
        stow = Stow(dest_bay, source_bay, weight, note)
        self._log.record(stow)
        return stow

    def log_entries(self):
        return self._log.stows()

    def weight_summary(self):
        total_in = 0
        total_out = 0
        for stow in self._log.stows():
            total_in += stow.weight
            total_out += stow.weight
        return total_in, total_out
