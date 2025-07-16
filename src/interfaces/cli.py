"""Command-line interface for the multi-agent system."""

from __future__ import annotations

import asyncio
import os
import typer
from dotenv import load_dotenv
from composition_root import bootstrap_command_bus, AGENT_REGISTRY
from application.commands.agent_commands import (
    RunAgentCommand,
    RunAgentHandler,
    StartProjectCommand,
)
from application.commands.echo_command import EchoCommand
from application.commands.file_commands import CreateFileCommand, ReadFileCommand
from application.commands.shell_commands import ExecuteShellCommand
from application.agent_runner import AgentRunner
from domain.communication import Message
from infrastructure.communication import InMemoryCommunicationChannel
from infrastructure.llm_graph_transformer import LangChainGraphTransformer
from infrastructure.memory_graph import InMemoryGraphRepository

# --- Environment Loading ---
load_dotenv()

# --- Singletons ---
# These are created once and shared across the application.
COMMAND_BUS = bootstrap_command_bus()
# For now, we use an in-memory channel. This would be replaced by a real
# implementation (e.g., Google A2A) in a production scenario.
COMMUNICATION_CHANNEL = InMemoryCommunicationChannel()
GRAPH_REPOSITORY = InMemoryGraphRepository()

# --- LLMGraphTransformer Initialization ---
# This requires credentials, so we load them from the environment.
try:
    GRAPH_TRANSFORMER = LangChainGraphTransformer(
        neo4j_url=os.environ["NEO4J_URI"],
        neo4j_username=os.environ["NEO4J_USERNAME"],
        neo4j_password=os.environ["NEO4J_PASSWORD"],
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
except KeyError as e:
    print(f"Error: Environment variable {e} not set.")
    print(
        "Please create a .env file with NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, and OPENAI_API_KEY."
    )
    raise typer.Exit(code=1)

# --- Typer App ---
app = typer.Typer(
    help="A multi-agent system for software development.",
    add_completion=False,
)

# --- CLI Commands ---


@app.command()
def echo(text: str):
    """Prints the given text back to the console."""
    result = asyncio.run(COMMAND_BUS.execute(EchoCommand(text=text)))
    typer.echo(result)


@app.command("create-file")
def create_file(path: str, content: str):
    """Creates a file at the specified path with the given content."""
    result = asyncio.run(COMMAND_BUS.execute(CreateFileCommand(path=path, content=content)))
    typer.echo(result)


@app.command("read-file")
def read_file(path: str):
    """Reads and prints the content of the specified file."""
    result = asyncio.run(COMMAND_BUS.execute(ReadFileCommand(path=path)))
    typer.echo(result)


@app.command("execute-shell")
def execute_shell(command: str):
    """Executes a shell command."""
    result = asyncio.run(COMMAND_BUS.execute(ExecuteShellCommand(command=command)))
    typer.echo(result)


@app.command("start-project")
def start_project(
    goal: str = typer.Option(..., "--goal", help="The high-level goal of the project.")
):
    """
    Initiates a new project by sending a task to the Architect agent.
    """
    arx_agent_id = "arx-agent"

    async def send_task():
        project_command = StartProjectCommand(project_goal=goal)
        message = Message(
            sender_id="cli", receiver_id=arx_agent_id, content=project_command
        )
        await COMMUNICATION_CHANNEL.send(message)
        typer.echo(f"Project goal sent to agent '{arx_agent_id}'.")

    asyncio.run(send_task())


@app.command("run-agent")
def run_agent(
    role: str = typer.Option(..., "--role", help="The role of the agent to run.")
):
    """
    Runs an agent with a specific role until interrupted.
    """
    if role not in AGENT_REGISTRY:
        typer.echo(f"Error: No agent found for role '{role}'.")
        typer.echo(f"Available roles: {list(AGENT_REGISTRY.keys())}")
        raise typer.Exit(code=1)

    # --- Dynamic Agent and Handler Creation ---
    agent_class = AGENT_REGISTRY[role]
    agent_id = f"{role}-agent"

    # Special handling for agents with extra dependencies
    if role == "arx":
        agent = agent_class(
            agent_id=agent_id,
            command_bus=COMMAND_BUS,
            communication_channel=COMMUNICATION_CHANNEL,
            graph_repository=GRAPH_REPOSITORY,
            graph_transformer=GRAPH_TRANSFORMER,
        )
    else:
        agent = agent_class(
            agent_id=agent_id,
            command_bus=COMMAND_BUS,
            communication_channel=COMMUNICATION_CHANNEL,
        )

    runner = AgentRunner(agent)
    handler = RunAgentHandler(runner)

    # The handler is registered just-in-time for this specific agent instance.
    COMMAND_BUS.register(RunAgentCommand, handler)

    typer.echo(f"Starting agent with role: {role} (Press Ctrl+C to stop)")
    try:
        asyncio.run(COMMAND_BUS.execute(RunAgentCommand(role=role)))
    except KeyboardInterrupt:
        typer.echo(f"\nStopping agent {role}...")
        runner.stop()
    finally:
        typer.echo(f"Agent {role} has been shut down.")


if __name__ == "__main__":
    app()
