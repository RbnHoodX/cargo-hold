"""Standard vessel layout presets."""

from layouts.symmetric import SymmetricLayout
from layouts.asymmetric import AsymmetricLayout


STANDARD_LAYOUTS = {
    "small-vessel": {
        "type": "symmetric",
        "sections": 2,
        "bays_per_section": 1,
        "description": "Small vessel with 4 bays",
    },
    "medium-vessel": {
        "type": "symmetric",
        "sections": 3,
        "bays_per_section": 2,
        "description": "Medium vessel with 12 bays",
    },
    "large-vessel": {
        "type": "symmetric",
        "sections": 5,
        "bays_per_section": 3,
        "description": "Large vessel with 30 bays",
    },
    "tanker": {
        "type": "asymmetric",
        "config": {"FORE": 2, "MID-A": 4, "MID-B": 4, "AFT": 2},
        "description": "Tanker configuration with large midship holds",
    },
    "container-ship": {
        "type": "asymmetric",
        "config": {"BOW": 3, "FORE": 6, "MID": 8, "AFT": 6, "STERN": 2},
        "description": "Container ship with tiered sections",
    },
    "bulk-carrier": {
        "type": "asymmetric",
        "config": {"FORE": 3, "MID": 5, "AFT": 3},
        "description": "Bulk carrier with dominant midship holds",
    },
}


def get_layout(name):
    """Get a layout instance by preset name.

    Args:
        name: The preset name from STANDARD_LAYOUTS.

    Returns:
        A SymmetricLayout or AsymmetricLayout instance.

    Raises:
        KeyError: If the preset name is not found.
    """
    if name not in STANDARD_LAYOUTS:
        raise KeyError(f"unknown layout preset: {name!r}")
    preset = STANDARD_LAYOUTS[name]
    if preset["type"] == "symmetric":
        return SymmetricLayout(
            sections=preset["sections"],
            bays_per_section=preset["bays_per_section"],
        )
    elif preset["type"] == "asymmetric":
        return AsymmetricLayout(section_config=preset["config"])
    else:
        raise ValueError(f"unknown layout type: {preset['type']!r}")


def list_presets():
    """List all available layout presets with descriptions."""
    results = []
    for name, info in STANDARD_LAYOUTS.items():
        results.append((name, info["description"]))
    return results


def preset_bay_count(name):
    """Get the total bay count for a preset."""
    layout = get_layout(name)
    return layout.total_bays
