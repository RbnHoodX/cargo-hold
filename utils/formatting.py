"""Formatting utilities for display output."""

from config import WEIGHT_PRECISION, HEADER_WIDTH


def format_weight(weight, unit="tons", precision=None):
    """Format a weight value with unit."""
    if precision is None:
        precision = WEIGHT_PRECISION
    if isinstance(weight, int):
        return f"{weight} {unit}"
    return f"{weight:.{precision}f} {unit}"


def format_bay_status(bay):
    """Format a bay's status as a string."""
    kind_tag = f" [{bay.kind}]" if bay.kind != "standard" else ""
    return f"{bay.name}{kind_tag}: {format_weight(bay.load)}"


def format_stow_entry(stow):
    """Format a stow log entry as a string."""
    parts = [
        f"#{stow.id}:",
        f"{stow.source_bay.name} -> {stow.dest_bay.name}",
        f"({format_weight(stow.weight)})",
    ]
    if stow.note:
        parts.append(f"[{stow.note}]")
    return " ".join(parts)


def format_header(title, width=None):
    """Format a section header."""
    if width is None:
        width = HEADER_WIDTH
    return f"{'=' * width}\n{title.center(width)}\n{'=' * width}"


def format_separator(width=None):
    """Format a separator line."""
    if width is None:
        width = HEADER_WIDTH
    return "-" * width


def format_bay_table(bays):
    """Format a list of bays as an aligned table."""
    if not bays:
        return "No bays."
    max_name = max(len(b.name) for b in bays)
    max_kind = max(len(b.kind) for b in bays)
    lines = []
    header = f"{'Name':<{max_name}}  {'Kind':<{max_kind}}  {'Load':>10}"
    lines.append(header)
    lines.append("-" * len(header))
    for bay in bays:
        lines.append(
            f"{bay.name:<{max_name}}  {bay.kind:<{max_kind}}  "
            f"{bay.load:>10}"
        )
    return "\n".join(lines)


def format_log_table(entries, limit=None):
    """Format stow log entries as a table."""
    if not entries:
        return "No log entries."
    if limit:
        entries = entries[:limit]
    lines = []
    header = f"{'ID':>4}  {'Source':<12}  {'Dest':<12}  {'Weight':>8}  {'Note'}"
    lines.append(header)
    lines.append("-" * len(header))
    for stow in entries:
        lines.append(
            f"{stow.id:>4}  {stow.source_bay.name:<12}  "
            f"{stow.dest_bay.name:<12}  {stow.weight:>8}  {stow.note}"
        )
    return "\n".join(lines)


def truncate(text, max_length=50):
    """Truncate text to a maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
