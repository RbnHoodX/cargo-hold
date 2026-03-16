"""Manifest formatting for display and export."""

import json
from config import DEFAULT_SEPARATOR, HEADER_WIDTH


class ManifestFormatter:
    """Formats manifest data for various output formats."""

    def __init__(self, separator=None, width=None):
        self._separator = separator or DEFAULT_SEPARATOR
        self._width = width or HEADER_WIDTH

    def format_text(self, manifest):
        """Format a manifest as plain text."""
        lines = []
        lines.append("=" * self._width)
        lines.append("CARGO MANIFEST")
        lines.append("=" * self._width)

        if "metadata" in manifest:
            for key, value in manifest["metadata"].items():
                lines.append(f"  {key}: {value}")
            lines.append("-" * self._width)

        if "bays" in manifest:
            for bay_data in manifest["bays"]:
                if isinstance(bay_data, dict):
                    name = bay_data.get("bay", bay_data.get("name", "?"))
                    load = bay_data.get("current_load", bay_data.get("load", 0))
                    lines.append(f"\n  Bay: {name} (Load: {load})")
                    if "entries" in bay_data:
                        for entry in bay_data["entries"]:
                            direction = entry.get("direction", "?")
                            weight = entry.get("weight", 0)
                            note = entry.get("note", "")
                            line = f"    [{direction}] {weight} tons"
                            if note:
                                line += f" ({note})"
                            lines.append(line)

        if "total_load" in manifest:
            lines.append("-" * self._width)
            lines.append(f"  Total Load: {manifest['total_load']} tons")

        lines.append("=" * self._width)
        return "\n".join(lines)

    def format_json(self, manifest, indent=2):
        """Format a manifest as JSON."""
        return json.dumps(manifest, indent=indent)

    def format_csv(self, manifest):
        """Format a manifest as CSV lines."""
        lines = []
        if "entries" in manifest:
            lines.append("id,source,dest,weight,note")
            for entry in manifest["entries"]:
                lines.append(
                    f"{entry['id']},{entry['source']},{entry['dest']},"
                    f"{entry['weight']},{entry.get('note', '')}"
                )
        elif "bays" in manifest:
            lines.append("bay,kind,load,stow_count")
            for bay in manifest["bays"]:
                name = bay.get("bay", bay.get("name", "?"))
                kind = bay.get("kind", "?")
                load = bay.get("current_load", bay.get("load", 0))
                count = bay.get("entry_count", bay.get("stow_count", 0))
                lines.append(f"{name},{kind},{load},{count}")
        return "\n".join(lines)

    def format_table(self, manifest):
        """Format a manifest as an aligned table."""
        if "bays" not in manifest:
            return self.format_text(manifest)

        headers = ["Bay", "Kind", "Load", "Entries"]
        rows = []
        for bay in manifest["bays"]:
            name = bay.get("bay", bay.get("name", "?"))
            kind = bay.get("kind", "?")
            load = str(bay.get("current_load", bay.get("load", 0)))
            count = str(bay.get("entry_count", bay.get("stow_count", 0)))
            rows.append([name, kind, load, count])

        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))

        header_line = self._separator.join(
            h.ljust(col_widths[i]) for i, h in enumerate(headers)
        )
        separator_line = "-" * len(header_line)
        lines = [header_line, separator_line]
        for row in rows:
            lines.append(self._separator.join(
                cell.ljust(col_widths[i]) for i, cell in enumerate(row)
            ))
        return "\n".join(lines)
