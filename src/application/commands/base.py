from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

T = TypeVar("T", bound="Command")


class Command:
    """A base class for commands, acting as a data carrier."""

    pass


class CommandHandler(ABC, Generic[T]):
    """Abstract base class for a command handler."""

    @abstractmethod
    async def handle(self, command: T) -> Any:
        """
        Handles the given command.

        Args:
            command: The command to handle.

        Returns:
            The result of the command execution.
        """
        pass


class CommandBus:
    """A simple command bus to dispatch commands to their handlers."""

    def __init__(self):
        self._handlers: Dict[type, CommandHandler] = {}

    def register(self, command_type: type, handler: CommandHandler):
        """Registers a handler for a specific command type."""
        self._handlers[command_type] = handler

    async def execute(self, command: Command) -> Any:
        """Executes a command by dispatching it to the registered handler."""
        handler = self._handlers.get(type(command))
        if not handler:
            raise TypeError(
                f"No handler registered for command type {type(command).__name__}"
            )
        return await handler.handle(command)
