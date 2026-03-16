"""Search utilities for finding stows and bays."""


def find_stows_by_note(hold, note_pattern):
    """Find stow entries whose note contains the given pattern."""
    pattern = note_pattern.lower()
    results = []
    for stow in hold.log_entries():
        if pattern in stow.note.lower():
            results.append(stow)
    return results


def find_stows_by_weight_range(hold, min_weight, max_weight):
    """Find stows within a weight range (inclusive)."""
    results = []
    for stow in hold.log_entries():
        if min_weight <= stow.weight <= max_weight:
            results.append(stow)
    return results


def find_bays_by_kind(hold, kind):
    """Find bays of a specific kind."""
    return [bay for bay in hold.bays() if bay.kind == kind]


def find_bays_by_load_range(hold, min_load, max_load):
    """Find bays whose current load falls within a range."""
    return [bay for bay in hold.bays() if min_load <= bay.load <= max_load]


def find_empty_bays(hold):
    """Find bays with zero load."""
    return [bay for bay in hold.bays() if bay.load == 0]


def find_stows_between_bays(hold, bay_name_a, bay_name_b):
    """Find all stows between two specific bays (in either direction)."""
    results = []
    for stow in hold.log_entries():
        names = {stow.source_bay.name, stow.dest_bay.name}
        if bay_name_a in names and bay_name_b in names:
            results.append(stow)
    return results


def find_heaviest_stow(hold):
    """Find the stow with the largest weight."""
    entries = hold.log_entries()
    if not entries:
        return None
    return max(entries, key=lambda s: s.weight)


def find_lightest_stow(hold):
    """Find the stow with the smallest weight."""
    entries = hold.log_entries()
    if not entries:
        return None
    return min(entries, key=lambda s: s.weight)


def count_stows_per_bay(hold):
    """Count the number of stow records per bay."""
    counts = {}
    for bay in hold.bays():
        counts[bay.name] = len(bay.stows())
    return counts


def find_most_active_bay(hold):
    """Find the bay involved in the most stow operations."""
    counts = count_stows_per_bay(hold)
    if not counts:
        return None
    return max(counts.items(), key=lambda x: x[1])
