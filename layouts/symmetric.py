"""Symmetric bay layout configuration."""


class SymmetricLayout:
    """A layout where bays are mirrored port and starboard."""

    def __init__(self, sections=3, bays_per_section=2):
        self._sections = sections
        self._bays_per_section = bays_per_section

    @property
    def sections(self):
        return self._sections

    @property
    def bays_per_section(self):
        return self._bays_per_section

    @property
    def total_bays(self):
        return self._sections * self._bays_per_section * 2

    def bay_names(self):
        """Generate bay names for this layout."""
        section_names = ["FORE", "MID", "AFT"]
        if self._sections > 3:
            section_names = [f"SEC-{i+1}" for i in range(self._sections)]
        names = []
        for sec in section_names[:self._sections]:
            for i in range(self._bays_per_section):
                names.append(f"{sec}-P{i+1}")
                names.append(f"{sec}-S{i+1}")
        return names

    def apply(self, hold):
        """Apply this layout to a hold, creating all bays."""
        for name in self.bay_names():
            hold.create_bay(name, "standard")
        return hold

    def port_bays(self):
        """Return names of port-side bays."""
        return [n for n in self.bay_names() if "-P" in n]

    def starboard_bays(self):
        """Return names of starboard-side bays."""
        return [n for n in self.bay_names() if "-S" in n]

    def section_bays(self, section_index):
        """Return bay names for a specific section."""
        all_names = self.bay_names()
        start = section_index * self._bays_per_section * 2
        end = start + self._bays_per_section * 2
        return all_names[start:end]

    def __repr__(self):
        return (f"SymmetricLayout(sections={self._sections}, "
                f"bays_per_section={self._bays_per_section})")
