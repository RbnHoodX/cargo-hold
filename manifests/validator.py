"""Manifest validation utilities."""


class ManifestValidator:
    """Validates manifest data for completeness and correctness."""

    def __init__(self, hold=None):
        self._hold = hold
        self._errors = []

    @property
    def errors(self):
        return list(self._errors)

    def validate_bay_manifest(self, manifest):
        """Validate a single bay manifest."""
        self._errors = []
        if "bay" not in manifest:
            self._errors.append("missing 'bay' field")
        if "entries" not in manifest:
            self._errors.append("missing 'entries' field")
        if "current_load" not in manifest:
            self._errors.append("missing 'current_load' field")

        if "entries" in manifest:
            for i, entry in enumerate(manifest["entries"]):
                if "id" not in entry:
                    self._errors.append(f"entry {i}: missing 'id'")
                if "direction" not in entry:
                    self._errors.append(f"entry {i}: missing 'direction'")
                elif entry["direction"] not in ("IN", "OUT"):
                    self._errors.append(
                        f"entry {i}: invalid direction {entry['direction']!r}"
                    )
                if "weight" not in entry:
                    self._errors.append(f"entry {i}: missing 'weight'")
                elif entry["weight"] <= 0:
                    self._errors.append(
                        f"entry {i}: weight must be positive"
                    )

        return len(self._errors) == 0

    def validate_full_manifest(self, manifest):
        """Validate a complete manifest."""
        self._errors = []
        if "bays" not in manifest:
            self._errors.append("missing 'bays' field")
            return False

        for i, bay_manifest in enumerate(manifest["bays"]):
            sub_validator = ManifestValidator()
            if not sub_validator.validate_bay_manifest(bay_manifest):
                for err in sub_validator.errors:
                    self._errors.append(f"bay {i}: {err}")

        if "total_load" in manifest and "bays" in manifest:
            computed = sum(
                b.get("current_load", 0) for b in manifest["bays"]
            )
            if computed != manifest["total_load"]:
                self._errors.append(
                    f"total_load mismatch: stated {manifest['total_load']}, "
                    f"computed {computed}"
                )

        return len(self._errors) == 0

    def validate_log_manifest(self, manifest):
        """Validate a log-based manifest."""
        self._errors = []
        if "entries" not in manifest:
            self._errors.append("missing 'entries' field")
            return False

        seen_ids = set()
        for i, entry in enumerate(manifest["entries"]):
            if "id" not in entry:
                self._errors.append(f"entry {i}: missing 'id'")
            elif entry["id"] in seen_ids:
                self._errors.append(f"entry {i}: duplicate id {entry['id']}")
            else:
                seen_ids.add(entry["id"])
            if "source" not in entry:
                self._errors.append(f"entry {i}: missing 'source'")
            if "dest" not in entry:
                self._errors.append(f"entry {i}: missing 'dest'")

        return len(self._errors) == 0

    def cross_validate(self, manifest):
        """Cross-validate manifest against the hold if available."""
        if self._hold is None:
            self._errors = ["no hold provided for cross-validation"]
            return False
        self._errors = []
        if "bays" in manifest:
            for bay_data in manifest["bays"]:
                name = bay_data.get("bay", bay_data.get("name"))
                if name:
                    try:
                        actual_bay = self._hold.get_bay(name)
                        if bay_data.get("current_load") != actual_bay.load:
                            self._errors.append(
                                f"bay {name}: load mismatch "
                                f"(manifest={bay_data.get('current_load')}, "
                                f"actual={actual_bay.load})"
                            )
                    except KeyError:
                        self._errors.append(f"bay {name}: not found in hold")
        return len(self._errors) == 0
