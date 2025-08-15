# src/composition_root.py

from typing import Dict, Callable, Tuple, Optional
from application.agents.data_architect.agent import DataArchitectAgent
from application.agents.data_engineer.agent import DataEngineerAgent
from application.agents.knowledge_manager.agent import KnowledgeManagerAgent
from application.agents.data_engineer.handlers.build_kg import BuildKGCommandHandler
from application.agents.echo_agent import EchoAgent
from application.agents.knowledge_manager.agent import KnowledgeManagerAgent
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
from application.commands.modeling_command import ModelingCommand
from application.commands.modeling_handler import ModelingCommandHandler
from application.agents.data_architect.modeling_workflow import ModelingWorkflow
from application.agents.data_architect.dda_parser import DDAParserFactory
from application.agents.data_architect.domain_modeler import DomainModeler
from infrastructure.parsers.markdown_parser import MarkdownDDAParser
from domain.agent import Agent
from domain.communication import CommunicationChannel
from infrastructure.graphiti import get_graphiti
from graphiti_core import Graphiti
from infrastructure.in_memory_backend import InMemoryGraphBackend
from application.event_bus import EventBus


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
    kg_backend: Optional[InMemoryGraphBackend] = None,
    event_bus: Optional[EventBus] = None,
) -> DataArchitectAgent:
    """Creates a DataArchitectAgent with a namespaced Graphiti graph and LLM."""
    return DataArchitectAgent(
        agent_id=agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
        graph=graph,
        llm=graph,  # Use Graphiti for both graph and LLM
        url=url,
        kg_backend=kg_backend,
        event_bus=event_bus,
    )

def create_data_engineer_agent(
    agent_id: str,
    command_bus: CommandBus,
    communication_channel: CommunicationChannel,
    graph: Graphiti,
    url: str,
    kg_backend: Optional[InMemoryGraphBackend] = None,
    event_bus: Optional[EventBus] = None,
) -> DataEngineerAgent:
    """Creates a DataEngineerAgent with a namespaced Graphiti graph."""
    return DataEngineerAgent(
        agent_id=agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
        graph=graph,
        url=url,
        kg_backend=kg_backend,
        event_bus=event_bus,
    )

def create_knowledge_manager_agent(
    agent_id: str,
    command_bus: CommandBus,
    communication_channel: CommunicationChannel,
    kg_backend: Optional[InMemoryGraphBackend] = None,
    event_bus: Optional[EventBus] = None,
) -> KnowledgeManagerAgent:
    """Creates a KnowledgeManagerAgent for complex knowledge graph operations."""
    # Use in-memory backend if none provided
    if kg_backend is None:
        kg_backend = InMemoryGraphBackend()
    
    # Use in-memory event bus if none provided
    if event_bus is None:
        event_bus = EventBus()
    
    return KnowledgeManagerAgent(
        agent_id=agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
        backend=kg_backend,
        event_bus=event_bus,
    )

def create_knowledge_manager_agent(
    agent_id: str,
    command_bus: CommandBus,
    communication_channel: CommunicationChannel,
    graph: Graphiti,
    url: str,
) -> KnowledgeManagerAgent:
    """Creates a KnowledgeManagerAgent for handling escalated KG operations."""
    return KnowledgeManagerAgent(
        graph=graph,
        llm=graph,  # Use Graphiti for both graph and LLM
    )

def create_modeling_command_handler(graph: Graphiti) -> ModelingCommandHandler:
    """Creates a ModelingCommandHandler with all necessary dependencies."""
    # Create parser factory and register parsers
    parser_factory = DDAParserFactory()
    markdown_parser = MarkdownDDAParser()
    parser_factory.register_parser(markdown_parser)
    
    # Create domain modeler
    domain_modeler = DomainModeler(graph, graph)  # Use Graphiti for both graph and LLM
    
    # Create modeling workflow
    modeling_workflow = ModelingWorkflow(parser_factory, domain_modeler)
    
    return ModelingCommandHandler(modeling_workflow)


# Agent Registry
# Maps a role name to an agent factory function.
AGENT_REGISTRY: Dict[str, Callable[..., Agent]] = {
    "data_architect": create_data_architect_agent,
    "data_engineer": create_data_engineer_agent,
    "knowledge_manager": create_knowledge_manager_agent,
    "echo": create_echo_agent,
    "knowledge_manager": create_knowledge_manager_agent,
}


async def bootstrap_graphiti(agent_name: str | None = None) -> Graphiti:
    """Initializes the Graphiti instance from environment variables, namespaced by agent if agent_name is provided."""
    from dotenv import load_dotenv
    import os

    load_dotenv()

    graph_config = {
        "uri": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.environ.get("NEO4J_USERNAME", os.environ.get("NEO4J_USER", "neo4j")),
        "password": os.environ.get("NEO4J_PASSWORD", "password"),
    }
    if agent_name:
        graph_config["name"] = agent_name
    return await get_graphiti(graph_config)


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
    # Note: BuildKGCommand and ModelingCommand handlers require Graphiti instances
    # and are registered dynamically when needed in the CLI or agent creation
    
    # Note: RunAgentHandler is registered dynamically in the CLI
    # because it depends on a runtime agent instance.

    return command_bus


def bootstrap_knowledge_management() -> Tuple[InMemoryGraphBackend, EventBus]:
    """Initialize knowledge management components."""
    kg_backend = InMemoryGraphBackend()
    event_bus = EventBus()
    
    return kg_backend, event_bus
