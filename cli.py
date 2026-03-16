"""Command-line interface for managing the cargo hold."""

import sys
from hold import Hold
from config import VALID_BAY_KINDS, MAX_BAY_LOAD


def create_sample_hold():
    """Create a hold with sample bays for demonstration."""
    hold = Hold()
    hold.create_bay("FORE-1", "standard")
    hold.create_bay("FORE-2", "standard")
    hold.create_bay("MID-1", "standard")
    hold.create_bay("MID-2", "standard")
    hold.create_bay("AFT-1", "standard")
    hold.create_bay("AFT-2", "overflow")
    return hold


def print_bay_status(hold):
    """Display the current status of all bays."""
    print("=" * 50)
    print("CARGO HOLD STATUS")
    print("=" * 50)
    for bay in hold.bays():
        load = bay.load
        kind_tag = f" [{bay.kind}]" if bay.kind != "standard" else ""
        print(f"  {bay.name}{kind_tag}: {load} tons")
    print("-" * 50)


def print_log(hold, limit=20):
    """Display recent stow log entries."""
    entries = hold.log_entries()
    if not entries:
        print("No stow entries recorded.")
        return
    print(f"\nRecent log entries (showing last {min(limit, len(entries))}):")
    for entry in entries[-limit:]:
        print(f"  #{entry.id}: {entry.source_bay.name} -> "
              f"{entry.dest_bay.name} ({entry.weight} tons)"
              f"{' [' + entry.note + ']' if entry.note else ''}")


def run_demo():
    """Run a demonstration of the cargo hold system."""
    hold = create_sample_hold()

    print("Loading cargo into bays...")
    hold.move("FORE-1", "AFT-2", 500, "initial load")
    hold.move("FORE-2", "AFT-2", 300, "initial load")
    hold.move("MID-1", "AFT-2", 750, "initial load")
    hold.move("MID-2", "AFT-2", 200, "initial load")
    hold.move("AFT-1", "AFT-2", 400, "initial load")

    print_bay_status(hold)

    print("\nRebalancing cargo...")
    hold.move("MID-2", "FORE-1", 100, "rebalance")
    hold.move("AFT-1", "MID-1", 250, "rebalance")

    print_bay_status(hold)
    print_log(hold)

    total_in, total_out = hold.weight_summary()
    print(f"\nWeight summary: {total_in} tons moved in, {total_out} tons moved out")


def main():
    """Entry point for the CLI."""
    args = sys.argv[1:]

    if not args or args[0] == "demo":
        run_demo()
    elif args[0] == "status":
        hold = create_sample_hold()
        print_bay_status(hold)
    elif args[0] == "help":
        print("Usage: python cli.py [command]")
        print("Commands:")
        print("  demo    - Run a demonstration")
        print("  status  - Show bay status")
        print("  help    - Show this help message")
    else:
        print(f"Unknown command: {args[0]}")
        print("Run 'python cli.py help' for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
