"""Aggregation utilities for hold data analysis."""


def sum_loads(hold):
    """Sum all bay loads in the hold."""
    return sum(bay.load for bay in hold.bays())


def group_by_kind(hold):
    """Group bays by their kind.

    Returns:
        Dict mapping kind strings to lists of bays.
    """
    groups = {}
    for bay in hold.bays():
        if bay.kind not in groups:
            groups[bay.kind] = []
        groups[bay.kind].append(bay)
    return groups


def average_load(hold):
    """Calculate the average load across all bays."""
    bays = hold.bays()
    if not bays:
        return 0
    return sum_loads(hold) / len(bays)


def max_load_bay(hold):
    """Find the bay with the highest load."""
    bays = hold.bays()
    if not bays:
        return None
    return max(bays, key=lambda b: b.load)


def min_load_bay(hold):
    """Find the bay with the lowest load."""
    bays = hold.bays()
    if not bays:
        return None
    return min(bays, key=lambda b: b.load)


def load_spread(hold):
    """Calculate the difference between max and min load."""
    bays = hold.bays()
    if not bays:
        return 0
    loads = [b.load for b in bays]
    return max(loads) - min(loads)


def weight_by_note(hold):
    """Aggregate total weight by stow note.

    Returns:
        Dict mapping note strings to total weight.
    """
    totals = {}
    for stow in hold.log_entries():
        note = stow.note or "(no note)"
        if note not in totals:
            totals[note] = 0
        totals[note] += stow.weight
    return totals


def stow_count_by_bay(hold):
    """Count stow operations per bay.

    Returns:
        Dict mapping bay names to stow counts.
    """
    counts = {}
    for bay in hold.bays():
        counts[bay.name] = len(bay.stows())
    return counts


def cumulative_weights(hold):
    """Calculate cumulative weight moved over time.

    Returns:
        List of (stow_id, cumulative_weight) tuples.
    """
    result = []
    running = 0
    for stow in hold.log_entries():
        running += stow.weight
        result.append((stow.id, running))
    return result


def bay_load_percentages(hold):
    """Calculate each bay's load as a percentage of total.

    Returns:
        Dict mapping bay names to load percentages.
    """
    total = sum_loads(hold)
    if total == 0:
        return {bay.name: 0.0 for bay in hold.bays()}
    return {bay.name: round(bay.load / total * 100, 2)
            for bay in hold.bays()}
