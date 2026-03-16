class Stow:
    """A cargo movement entry linking two bays."""

    def __init__(self, dest_bay, source_bay, weight, note=""):
        self._id = 0
        self._dest_bay = dest_bay
        self._source_bay = source_bay
        self._weight = weight
        self._note = note

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def dest_bay(self):
        return self._dest_bay

    @property
    def source_bay(self):
        return self._source_bay

    @property
    def weight(self):
        return self._weight

    @property
    def note(self):
        return self._note

    def __repr__(self):
        return (f"Stow(id={self._id}, dest={self._dest_bay.name!r}, "
                f"source={self._source_bay.name!r}, weight={self._weight})")


class StowLog:
    """Append-only log of cargo stow records."""

    def __init__(self):
        self._stows = []
        self._counter = 0

    def record(self, stow):
        self._counter += 1
        stow.id = self._counter
        self._stows.append(stow)
        stow.dest_bay._add_stow(stow)
        stow.source_bay._add_stow(stow)
        return stow

    def stows(self):
        return list(self._stows)
