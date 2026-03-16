"""Seed a cargo hold with sample data for testing and demonstration."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hold import Hold


def create_seeded_hold():
    """Create a hold with sample bays and cargo movements."""
    hold = Hold()

    # Create bays
    hold.create_bay("FORE-1", "standard")
    hold.create_bay("FORE-2", "standard")
    hold.create_bay("MID-1", "standard")
    hold.create_bay("MID-2", "standard")
    hold.create_bay("AFT-1", "standard")
    hold.create_bay("AFT-2", "overflow")
    hold.create_bay("DECK-1", "standard")
    hold.create_bay("DECK-2", "overflow")

    # Initial loading from overflow bays
    hold.move("FORE-1", "DECK-2", 500, "initial")
    hold.move("FORE-2", "DECK-2", 350, "initial")
    hold.move("MID-1", "DECK-2", 800, "initial")
    hold.move("MID-2", "DECK-2", 250, "initial")
    hold.move("AFT-1", "AFT-2", 600, "initial")
    hold.move("AFT-2", "DECK-2", 100, "initial")
    hold.move("DECK-1", "DECK-2", 450, "initial")

    # Rebalancing moves
    hold.move("MID-2", "FORE-1", 200, "rebalance")
    hold.move("AFT-1", "MID-1", 150, "rebalance")
    hold.move("FORE-2", "DECK-1", 100, "rebalance")

    # Additional cargo
    hold.move("MID-1", "AFT-2", 300, "additional")
    hold.move("DECK-1", "AFT-2", 200, "additional")

    return hold


def print_hold_status(hold):
    """Print the current state of the hold."""
    print("Cargo Hold Status")
    print("=" * 40)
    for bay in hold.bays():
        print(f"  {bay.name} ({bay.kind}): {bay.load} tons")
    print("-" * 40)
    total_in, total_out = hold.weight_summary()
    print(f"Total moved: {total_in} tons")
    print(f"Log entries: {len(hold.log_entries())}")


if __name__ == "__main__":
    hold = create_seeded_hold()
    print_hold_status(hold)
