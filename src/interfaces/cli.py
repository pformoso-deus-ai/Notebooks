"""Command-line interface for the multi-agent system."""

from __future__ import annotations

import asyncio
import os
import typer
from dotenv import load_dotenv
from composition_root import (
    bootstrap_command_bus,
    bootstrap_graphiti,
    AGENT_REGISTRY,
)
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
from src.infrastructure.communication.memory_channel import InMemoryCommunicationChannel

# --- Environment Loading ---
load_dotenv()

# --- Singletons ---
# These are created once and shared across the application.
COMMAND_BUS = bootstrap_command_bus()
# For now, we use an in-memory channel. This would be replaced by a real
# implementation (e.g., Google A2A) in a production scenario.
COMMUNICATION_CHANNEL = InMemoryCommunicationChannel()


# --- Typer App ---
app = typer.Typer(
    help="A multi-agent system for software development.",
    add_completion=False,
)

# --- CLI Commands ---


@app.command()
def echo(text: str):
    """Prints the given text back to the console."""
    result = asyncio.run(COMMAND_BUS.dispatch(EchoCommand(text=text)))
    typer.echo(result)


@app.command("create-file")
def create_file(path: str, content: str):
    """Creates a file at the specified path with the given content."""
    result = asyncio.run(COMMAND_BUS.dispatch(CreateFileCommand(path=path, content=content)))
    typer.echo(result)


@app.command("read-file")
def read_file(path: str):
    """Reads and prints the content of the specified file."""
    result = asyncio.run(COMMAND_BUS.dispatch(ReadFileCommand(path=path)))
    typer.echo(result)


@app.command("execute-shell")
def execute_shell(command: str):
    """Executes a shell command."""
    result = asyncio.run(COMMAND_BUS.dispatch(ExecuteShellCommand(command=command)))
    typer.echo(result)


@app.command("start-project")
def start_project(
    goal: str = typer.Option(..., "--goal", help="The high-level goal of the project.")
):
    """
    Initiates a new project by sending a task to the Architect agent.
    """
    arx_agent_id = "data_architect-agent"

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
    agent_factory = AGENT_REGISTRY[role]
    agent_id = f"{role}-agent"

    # Use agent_id as the namespace for Graphiti graph
    graph = bootstrap_graphiti(agent_id)

    # Special handling for agents with extra dependencies
    if role == "data_architect":
        agent = agent_factory(
            agent_id=agent_id,
            command_bus=COMMAND_BUS,
            communication_channel=COMMUNICATION_CHANNEL,
            graph=graph,
            llm=graph,  # Use Graphiti for both graph and LLM
            url="http://localhost:8001",
        )
    elif role == "data_engineer":
        agent = agent_factory(
            agent_id=agent_id,
            command_bus=COMMAND_BUS,
            communication_channel=COMMUNICATION_CHANNEL,
            graph=graph,
            url="http://localhost:8002",
        )
    else:
        agent = agent_factory(
            agent_id=agent_id,
            command_bus=COMMAND_BUS,
            communication_channel=COMMUNICATION_CHANNEL,
            url="http://localhost:8000",
        )

    runner = AgentRunner(agent)
    handler = RunAgentHandler(runner)

    # The handler is registered just-in-time for this specific agent instance.
    COMMAND_BUS.register(RunAgentCommand, handler)

    typer.echo(f"Starting agent with role: {role} (Press Ctrl+C to stop)")
    try:
        asyncio.run(COMMAND_BUS.dispatch(RunAgentCommand(role=role)))
    except KeyboardInterrupt:
        typer.echo(f"\nStopping agent {role}...")
        runner.stop()
    finally:
        typer.echo(f"Agent {role} has been shut down.")


if __name__ == "__main__":
    app()
