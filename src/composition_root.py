# src/composition_root.py

from typing import Dict, Type
from application.agents import ArxAgent, DeveloperAgent, EchoAgent
from application.commands.base import CommandBus
from application.commands.echo_command import EchoCommand, EchoCommandHandler
from application.commands.file_commands import (
    CreateFileCommand,
    CreateFileCommandHandler,
    ReadFileCommand,
    ReadFileCommandHandler,
)
from application.commands.shell_commands import (
    ExecuteShellCommand,
    ExecuteShellCommandHandler,
)
from domain.agent import Agent

# Agent Registry
# Maps a role name to an agent class.
AGENT_REGISTRY: Dict[str, Type[Agent]] = {
    "arx": ArxAgent,
    "dev": DeveloperAgent,
    "echo": EchoAgent,
}


def bootstrap_command_bus() -> CommandBus:
    """Initializes and registers all command handlers."""
    command_bus = CommandBus()

    # Register handlers
    command_bus.register(EchoCommand, EchoCommandHandler())
    command_bus.register(CreateFileCommand, CreateFileCommandHandler())
    command_bus.register(ReadFileCommand, ReadFileCommandHandler())
    command_bus.register(
        ExecuteShellCommand,
        ExecuteShellCommandHandler(),
    )
    # Note: RunAgentHandler is registered dynamically in the CLI
    # because it depends on a runtime agent instance.

    return command_bus
