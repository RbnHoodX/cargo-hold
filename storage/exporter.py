"""Export hold data to various file formats."""

import json
import csv
import io


class HoldExporter:
    """Exports hold data to files or strings in various formats."""

    def __init__(self, hold):
        self._hold = hold

    def to_csv_string(self):
        """Export bay summary as CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["bay_name", "kind", "load", "stow_count"])
        for bay in self._hold.bays():
            writer.writerow([bay.name, bay.kind, bay.load, len(bay.stows())])
        return output.getvalue()

    def to_json_string(self, indent=2):
        """Export hold state as JSON string."""
        data = {
            "bays": [],
            "log_entries": [],
        }
        for bay in self._hold.bays():
            data["bays"].append({
                "name": bay.name,
                "kind": bay.kind,
                "load": bay.load,
            })
        for stow in self._hold.log_entries():
            data["log_entries"].append({
                "id": stow.id,
                "source": stow.source_bay.name,
                "dest": stow.dest_bay.name,
                "weight": stow.weight,
                "note": stow.note,
            })
        return json.dumps(data, indent=indent)

    def to_text_report(self):
        """Export as a human-readable text report."""
        lines = ["CARGO HOLD EXPORT REPORT", "=" * 40, ""]

        lines.append("BAYS:")
        for bay in self._hold.bays():
            lines.append(f"  {bay.name} ({bay.kind}): {bay.load} tons")

        lines.append("")
        lines.append("STOW LOG:")
        for stow in self._hold.log_entries():
            lines.append(
                f"  #{stow.id}: {stow.source_bay.name} -> "
                f"{stow.dest_bay.name} ({stow.weight} tons)"
            )

        total_in, total_out = self._hold.weight_summary()
        lines.append("")
        lines.append(f"Total weight moved: {total_in} tons")

        return "\n".join(lines)

    def log_to_csv_string(self):
        """Export stow log as CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "source", "dest", "weight", "note"])
        for stow in self._hold.log_entries():
            writer.writerow([
                stow.id,
                stow.source_bay.name,
                stow.dest_bay.name,
                stow.weight,
                stow.note,
            ])
        return output.getvalue()

    def bay_stows_to_csv(self, bay_name):
        """Export stow entries for a specific bay as CSV."""
        bay = self._hold.get_bay(bay_name)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "direction", "weight", "counterpart", "note"])
        for stow in bay.stows():
            direction = "IN" if stow.dest_bay is bay else "OUT"
            counterpart = (stow.source_bay.name if direction == "IN"
                           else stow.dest_bay.name)
            writer.writerow([stow.id, direction, stow.weight, counterpart,
                             stow.note])
        return output.getvalue()
