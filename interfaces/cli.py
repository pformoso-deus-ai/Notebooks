"""Command-line interface for the multi-agent system."""

from __future__ import annotations

import argparse


def execute_command(command_name: str) -> None:
    """Execute a named command.

    Parameters
    ----------
    command_name:
        Name of the command to execute.
    """
    print(f"Executing: {command_name}")


def build_parser() -> argparse.ArgumentParser:
    """Create and return the top-level argument parser."""
    parser = argparse.ArgumentParser(prog="multi_agent_system")
    subparsers = parser.add_subparsers(dest="subcommand")

    exec_parser = subparsers.add_parser(
        "execute-command", help="Execute a registered command"
    )
    exec_parser.add_argument("name", help="Name of the command to run")
    exec_parser.set_defaults(func=lambda args: execute_command(args.name))

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point used by the console script and ``python -m``."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
