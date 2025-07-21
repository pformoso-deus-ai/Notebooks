"""Main entry point for the application."""

from interfaces.cli import app


def main():
    """Runs the command-line interface."""
    app()


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
