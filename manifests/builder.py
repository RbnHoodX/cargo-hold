"""Manifest builder for creating cargo manifests from hold data."""


class ManifestBuilder:
    """Builds cargo manifests from hold state and log data."""

    def __init__(self, hold):
        self._hold = hold
        self._metadata = {}

    def set_metadata(self, key, value):
        """Set a metadata field on the manifest."""
        self._metadata[key] = value

    def get_metadata(self, key, default=None):
        """Get a metadata field."""
        return self._metadata.get(key, default)

    def build_bay_manifest(self, bay_name):
        """Build a manifest for a single bay."""
        bay = self._hold.get_bay(bay_name)
        stows = bay.stows()
        entries = []
        for stow in stows:
            direction = "IN" if stow.dest_bay is bay else "OUT"
            entries.append({
                "id": stow.id,
                "direction": direction,
                "weight": stow.weight,
                "counterpart": (stow.source_bay.name if direction == "IN"
                                else stow.dest_bay.name),
                "note": stow.note,
            })
        return {
            "bay": bay_name,
            "kind": bay.kind,
            "current_load": bay.load,
            "entry_count": len(entries),
            "entries": entries,
        }

    def build_full_manifest(self):
        """Build a complete manifest for all bays."""
        manifests = []
        for bay in self._hold.bays():
            manifests.append(self.build_bay_manifest(bay.name))
        total_load = sum(m["current_load"] for m in manifests)
        return {
            "metadata": dict(self._metadata),
            "total_load": total_load,
            "bay_count": len(manifests),
            "bays": manifests,
        }

    def build_log_manifest(self):
        """Build a manifest from the stow log."""
        entries = []
        for stow in self._hold.log_entries():
            entries.append({
                "id": stow.id,
                "source": stow.source_bay.name,
                "dest": stow.dest_bay.name,
                "weight": stow.weight,
                "note": stow.note,
            })
        return {
            "metadata": dict(self._metadata),
            "entry_count": len(entries),
            "entries": entries,
        }

    def build_summary_manifest(self):
        """Build a summary-only manifest without individual entries."""
        bays_summary = []
        for bay in self._hold.bays():
            bays_summary.append({
                "name": bay.name,
                "kind": bay.kind,
                "load": bay.load,
                "stow_count": len(bay.stows()),
            })
        return {
            "metadata": dict(self._metadata),
            "bays": bays_summary,
            "total_load": sum(b["load"] for b in bays_summary),
        }
