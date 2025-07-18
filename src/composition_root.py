# src/composition_root.py

from typing import Dict, Callable, Tuple
from application.agents.data_architect.agent import DataArchitectAgent
from application.agents.data_engineer.agent import DataEngineerAgent
from application.agents.data_engineer.handlers.build_kg import BuildKGCommandHandler
from application.agents.echo_agent import EchoAgent
from application.commands.base import CommandBus
from src.application.commands.collaboration_commands import BuildKGCommand
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
from domain.communication import CommunicationChannel
from infrastructure.graphiti import get_graphiti
from graphiti_core import Graphiti
from graphiti.graph import Graph
from graphiti.llm import LLM


# --- Agent Factory Functions ---

def create_echo_agent(
    agent_id: str,
    command_bus: CommandBus,
    communication_channel: CommunicationChannel,
    url: str,
) -> EchoAgent:
    """Creates an EchoAgent. agent_id is used for namespacing if needed."""
    return EchoAgent(
        agent_id=agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
        url=url,
    )

def create_data_architect_agent(
    agent_id: str,
    command_bus: CommandBus,
    communication_channel: CommunicationChannel,
    graph: Graphiti,
    url: str,
) -> DataArchitectAgent:
    """Creates a DataArchitectAgent with a namespaced Graphiti graph and LLM."""
    return DataArchitectAgent(
        agent_id=agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
        graph=graph,
        llm=graph,  # Use Graphiti for both graph and LLM
        url=url,
    )

def create_data_engineer_agent(
    agent_id: str,
    command_bus: CommandBus,
    communication_channel: CommunicationChannel,
    graph: Graphiti,
    url: str,
) -> DataEngineerAgent:
    """Creates a DataEngineerAgent with a namespaced Graphiti graph."""
    return DataEngineerAgent(
        agent_id=agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
        graph=graph,
        url=url,
    )


# Agent Registry
# Maps a role name to an agent factory function.
AGENT_REGISTRY: Dict[str, Callable[..., Agent]] = {
    "data_architect": create_data_architect_agent,
    "data_engineer": create_data_engineer_agent,
    "echo": create_echo_agent,
}


def bootstrap_graphiti(agent_name: str = None) -> Graphiti:
    """Initializes the Graphiti instance from environment variables, namespaced by agent if agent_name is provided."""
    from dotenv import load_dotenv
    import os

    load_dotenv()

    graph_config = {
        "uri": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.environ.get("NEO4J_USER", "neo4j"),
        "password": os.environ.get("NEO4J_PASSWORD", "password"),
    }
    if agent_name:
        graph_config["name"] = agent_name
    return get_graphiti(graph_config)


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
    command_bus.register(BuildKGCommand, BuildKGCommandHandler())
    # Note: RunAgentHandler is registered dynamically in the CLI
    # because it depends on a runtime agent instance.

    return command_bus
