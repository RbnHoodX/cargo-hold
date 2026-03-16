"""Tests for standard layout presets."""

from layouts.standards import get_layout, list_presets, STANDARD_LAYOUTS


class TestStandardLayouts:
    def test_all_presets_exist(self):
        assert len(STANDARD_LAYOUTS) >= 4

    def test_get_small_vessel(self):
        layout = get_layout("small-vessel")
        assert layout.total_bays == 4

    def test_get_medium_vessel(self):
        layout = get_layout("medium-vessel")
        assert layout.total_bays == 12

    def test_get_unknown_raises(self):
        import pytest
        with pytest.raises(KeyError):
            get_layout("submarine")

    def test_list_presets(self):
        presets = list_presets()
        assert len(presets) >= 4
        names = [p[0] for p in presets]
        assert "small-vessel" in names
