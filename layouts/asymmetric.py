"""Asymmetric bay layout configuration."""


class AsymmetricLayout:
    """A layout with different bay counts per section."""

    def __init__(self, section_config=None):
        if section_config is None:
            section_config = {"FORE": 2, "MID": 4, "AFT": 3}
        self._section_config = dict(section_config)

    @property
    def sections(self):
        return list(self._section_config.keys())

    @property
    def total_bays(self):
        return sum(self._section_config.values())

    def bay_names(self):
        """Generate bay names based on section configuration."""
        names = []
        for section, count in self._section_config.items():
            for i in range(count):
                names.append(f"{section}-{i+1}")
        return names

    def apply(self, hold, overflow_sections=None):
        """Apply this layout to a hold.

        Args:
            hold: The Hold instance to configure.
            overflow_sections: Set of section names that should be overflow bays.
        """
        if overflow_sections is None:
            overflow_sections = set()
        for section, count in self._section_config.items():
            kind = "overflow" if section in overflow_sections else "standard"
            for i in range(count):
                hold.create_bay(f"{section}-{i+1}", kind)
        return hold

    def section_bay_count(self, section):
        """Get the number of bays in a section."""
        return self._section_config.get(section, 0)

    def add_section(self, name, count):
        """Add a new section to the layout."""
        if name in self._section_config:
            raise ValueError(f"section {name!r} already exists")
        self._section_config[name] = count

    def remove_section(self, name):
        """Remove a section from the layout."""
        if name not in self._section_config:
            raise KeyError(f"section {name!r} not found")
        del self._section_config[name]

    def resize_section(self, name, count):
        """Change the number of bays in a section."""
        if name not in self._section_config:
            raise KeyError(f"section {name!r} not found")
        if count < 1:
            raise ValueError("count must be at least 1")
        self._section_config[name] = count

    def __repr__(self):
        return f"AsymmetricLayout(sections={self._section_config})"
