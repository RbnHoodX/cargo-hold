"""Serialization utilities for hold data."""

import json


class HoldSerializer:
    """Serializes hold state to and from dictionaries."""

    def serialize_bay(self, bay):
        """Serialize a bay to a dictionary."""
        return {
            "name": bay.name,
            "kind": bay.kind,
            "load": bay.load,
            "stow_count": len(bay.stows()),
        }

    def serialize_stow(self, stow):
        """Serialize a stow record to a dictionary."""
        return {
            "id": stow.id,
            "dest_bay": stow.dest_bay.name,
            "source_bay": stow.source_bay.name,
            "weight": stow.weight,
            "note": stow.note,
        }

    def serialize_hold(self, hold):
        """Serialize the full hold state."""
        return {
            "bays": [self.serialize_bay(b) for b in hold.bays()],
            "log": [self.serialize_stow(s) for s in hold.log_entries()],
            "summary": {
                "bay_count": len(hold.bays()),
                "log_count": len(hold.log_entries()),
                "weight_summary": hold.weight_summary(),
            },
        }

    def to_json(self, hold, indent=2):
        """Serialize hold to JSON string."""
        data = self.serialize_hold(hold)
        return json.dumps(data, indent=indent)

    def serialize_bay_detail(self, bay):
        """Serialize a bay with full stow details."""
        stows = []
        for stow in bay.stows():
            direction = "IN" if stow.dest_bay is bay else "OUT"
            stows.append({
                "id": stow.id,
                "direction": direction,
                "weight": stow.weight,
                "counterpart": (stow.source_bay.name if direction == "IN"
                                else stow.dest_bay.name),
                "note": stow.note,
            })
        return {
            "name": bay.name,
            "kind": bay.kind,
            "load": bay.load,
            "stows": stows,
        }

    def snapshot(self, hold):
        """Create a lightweight snapshot of hold state."""
        return {
            "bays": {bay.name: bay.load for bay in hold.bays()},
            "log_size": len(hold.log_entries()),
        }
