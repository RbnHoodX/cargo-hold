class Bay:
    """A cargo bay that tracks its load from stow log entries.

    The load is always computed from stows -- never stored directly.
    This guarantees the load is always consistent with the stow log.
    """

    def __init__(self, name, kind="standard"):
        self._name = name
        self._kind = kind
        self._stows = []

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def load(self):
        total = 0
        for stow in self._stows:
            if stow.dest_bay is self:
                total += stow.weight
            elif stow.source_bay is self:
                total -= stow.weight
        return total

    def _add_stow(self, stow):
        self._stows.append(stow)

    def stows(self):
        return list(self._stows)

    def __repr__(self):
        return f"Bay(name={self._name!r}, kind={self._kind!r})"
