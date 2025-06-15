from dataclasses import dataclass
from .base import Command, CommandHandler


@dataclass
class EchoCommand(Command):
    """A simple command that echoes back the text it receives."""

    text: str


class EchoCommandHandler(CommandHandler[EchoCommand]):
    """The handler for the EchoCommand."""

    async def handle(self, command: EchoCommand) -> str:
        """Handles the command by returning the text."""
        print(f"Echoing: {command.text}")
        return command.text
