"""Load hold data from serialized formats."""

import json
from hold import Hold


class HoldLoader:
    """Loads hold state from serialized data."""

    def from_dict(self, data):
        """Restore a hold from a dictionary.

        Note: This recreates bays and replays stow log entries to
        rebuild the hold state. The loaded hold will have the same
        bay loads as the original.
        """
        hold = Hold()
        bay_kinds = {}

        if "bays" in data:
            for bay_data in data["bays"]:
                name = bay_data["name"]
                kind = bay_data.get("kind", "standard")
                hold.create_bay(name, kind)
                bay_kinds[name] = kind

        if "log" in data:
            for entry in data["log"]:
                hold.move(
                    entry["dest_bay"],
                    entry["source_bay"],
                    entry["weight"],
                    entry.get("note", ""),
                )

        return hold

    def from_json(self, json_string):
        """Restore a hold from a JSON string."""
        data = json.loads(json_string)
        return self.from_dict(data)

    def from_json_file(self, filepath):
        """Restore a hold from a JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        return self.from_dict(data)

    def from_bay_list(self, bay_configs):
        """Create a hold from a list of bay configurations.

        Args:
            bay_configs: List of dicts with 'name' and optional 'kind'.
        """
        hold = Hold()
        for config in bay_configs:
            hold.create_bay(
                config["name"],
                config.get("kind", "standard"),
            )
        return hold

    def validate_data(self, data):
        """Check if data is valid for loading.

        Returns:
            Tuple of (is_valid, errors).
        """
        errors = []
        if not isinstance(data, dict):
            return False, ["data must be a dictionary"]

        if "bays" not in data:
            errors.append("missing 'bays' key")
        else:
            bay_names = set()
            for i, bay in enumerate(data["bays"]):
                if "name" not in bay:
                    errors.append(f"bay {i}: missing 'name'")
                elif bay["name"] in bay_names:
                    errors.append(f"bay {i}: duplicate name {bay['name']!r}")
                else:
                    bay_names.add(bay["name"])

        if "log" in data:
            for i, entry in enumerate(data["log"]):
                if "dest_bay" not in entry:
                    errors.append(f"log entry {i}: missing 'dest_bay'")
                if "source_bay" not in entry:
                    errors.append(f"log entry {i}: missing 'source_bay'")
                if "weight" not in entry:
                    errors.append(f"log entry {i}: missing 'weight'")

        return len(errors) == 0, errors
