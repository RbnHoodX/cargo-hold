"""Validate a cargo hold's integrity."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hold import Hold


def validate_hold(hold):
    """Run integrity checks on a hold.

    Returns:
        Tuple of (is_valid, list of issues found).
    """
    issues = []

    # Check that bay loads match stow records
    for bay in hold.bays():
        computed_load = 0
        for stow in bay.stows():
            if stow.dest_bay is bay:
                computed_load += stow.weight
            elif stow.source_bay is bay:
                computed_load -= stow.weight
        if computed_load != bay.load:
            issues.append(
                f"Bay {bay.name}: load mismatch "
                f"(property={bay.load}, computed={computed_load})"
            )

    # Check stow log consistency
    seen_ids = set()
    for stow in hold.log_entries():
        if stow.id in seen_ids:
            issues.append(f"Duplicate stow id: {stow.id}")
        seen_ids.add(stow.id)
        if stow.weight <= 0:
            issues.append(f"Stow #{stow.id}: non-positive weight {stow.weight}")
        if stow.dest_bay is stow.source_bay:
            issues.append(f"Stow #{stow.id}: dest and source are same bay")

    # Check standard bay constraints
    for bay in hold.bays():
        if bay.kind == "standard" and bay.load < 0:
            issues.append(
                f"Bay {bay.name}: standard bay has negative load {bay.load}"
            )

    return len(issues) == 0, issues


def main():
    """Run validation on a sample hold."""
    hold = Hold()
    hold.create_bay("A", "standard")
    hold.create_bay("B", "standard")
    hold.create_bay("C", "overflow")

    hold.move("A", "C", 100)
    hold.move("B", "C", 200)
    hold.move("A", "B", 50)

    is_valid, issues = validate_hold(hold)
    if is_valid:
        print("Hold is valid.")
    else:
        print("Hold has issues:")
        for issue in issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
