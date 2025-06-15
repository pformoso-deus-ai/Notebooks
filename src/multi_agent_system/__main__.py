"""Main entry point for the application."""

from composition_root import build_command_bus
from interfaces.cli import main as cli_main


def main():
    """Builds dependencies and runs the command-line interface."""
    # 1. Build the application's command bus
    command_bus = build_command_bus()

    # 2. Run the CLI, injecting the command bus
    cli_main(bus=command_bus)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
