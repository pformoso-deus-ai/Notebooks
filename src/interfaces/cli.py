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
    create_modeling_command_handler,
)
from application.commands.agent_commands import (
    RunAgentCommand,
    RunAgentHandler,
    StartProjectCommand,
)
from application.commands.echo_command import EchoCommand
from application.commands.file_commands import CreateFileCommand, ReadFileCommand
from application.commands.shell_commands import ExecuteShellCommand
from application.commands.modeling_command import ModelingCommand
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


@app.command("model")
def model(
    dda_path: str = typer.Option(..., "--dda-path", help="Path to the DDA document"),
    domain: str = typer.Option(None, "--domain", help="Explicit domain specification"),
    update_existing: bool = typer.Option(False, "--update-existing", help="Update existing graph"),
    validate_only: bool = typer.Option(False, "--validate-only", help="Only validate without creating graph"),
    output_path: str = typer.Option(None, "--output-path", help="Path for output artifacts"),
):
    """Process DDA document and create/update knowledge graph."""
    
    async def run_modeling():
        # Create a temporary Graphiti instance for modeling
        graph = await bootstrap_graphiti("modeling-temp")
        
        # Register the modeling command handler
        modeling_handler = create_modeling_command_handler(graph)
        COMMAND_BUS.register(ModelingCommand, modeling_handler)
        
        # Create and execute the modeling command
        command = ModelingCommand(
            dda_path=dda_path,
            domain=domain,
            update_existing=update_existing,
            validate_only=validate_only,
            output_path=output_path
        )
        
        return await COMMAND_BUS.dispatch(command)
    
    result = asyncio.run(run_modeling())
    
    if result["success"]:
        typer.echo(f"✅ Modeling completed successfully!")
        typer.echo(f"   Domain: {result['graph_document'].get('domain', 'Unknown')}")
        typer.echo(f"   Entities: {result['graph_document'].get('entities_count', 0)}")
        typer.echo(f"   Relationships: {result['graph_document'].get('relationships_count', 0)}")
        typer.echo(f"   Nodes Created: {result['graph_document'].get('nodes_created', 0)}")
        typer.echo(f"   Edges Created: {result['graph_document'].get('edges_created', 0)}")
        typer.echo(f"   Episode UUID: {result['graph_document'].get('episode_uuid', 'N/A')}")
        
        # Show workflow state information
        if 'workflow_state' in result:
            workflow = result['workflow_state']
            if workflow.get('backup_created'):
                typer.echo(f"   Backup Created: {workflow.get('backup_path', 'N/A')}")
            if workflow.get('cache_hit'):
                typer.echo(f"   Cache Hit: Yes")
        
        if result.get('warnings'):
            typer.echo(f"   Warnings: {len(result['warnings'])}")
            for warning in result['warnings']:
                typer.echo(f"     - {warning}")
    else:
        typer.echo(f"❌ Modeling failed:")
        for error in result.get('errors', []):
            typer.echo(f"   - {error}")
        
        # Show workflow state for debugging
        if 'workflow_state' in result:
            workflow = result['workflow_state']
            typer.echo(f"   Steps Completed: {', '.join(workflow.get('steps_completed', []))}")
            if workflow.get('rollback_performed'):
                typer.echo(f"   Rollback Performed: Yes")
        
        raise typer.Exit(code=1)


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


@app.command("create-template")
def create_template(
    name: str = typer.Option(..., "--name", help="Name for the DDA template"),
    output_path: str = typer.Option(None, "--output-path", help="Output path for the template"),
):
    """Create a new DDA template with the given name."""
    
    template_content = f"""# Data Delivery Agreement (DDA) - {name}

## Document Information
- **Domain**: {name}
- **Stakeholders**: [List key stakeholders]
- **Data Owner**: [Data owner name/role]
- **Effective Date**: [YYYY-MM-DD]
- **Review Cycle**: [Monthly/Quarterly/Annually]

## Business Context
[Describe the business context and purpose of this domain]

## Data Entities

### [Entity Name]
- **Description**: [Entity description]
- **Key Attributes**:
  - [Attribute 1] (Primary Key)
  - [Attribute 2]
  - [Attribute 3]
- **Business Rules**:
  - [Business rule 1]
  - [Business rule 2]

### [Entity Name 2]
- **Description**: [Entity description]
- **Key Attributes**:
  - [Attribute 1] (Primary Key)
  - [Attribute 2] (Foreign Key)
  - [Attribute 3]
- **Business Rules**:
  - [Business rule 1]
  - [Business rule 2]

## Relationships

### [Relationship Category]
- **[Entity 1]** → **[Entity 2]** (1:N)
  - [Relationship description]
  - [Constraints]

- **[Entity 1]** → **[Entity 3]** (M:N)
  - [Relationship description]
  - [Constraints]

## Data Quality Requirements

### Completeness
- [Completeness requirement 1]
- [Completeness requirement 2]

### Accuracy
- [Accuracy requirement 1]
- [Accuracy requirement 2]

### Timeliness
- [Timeliness requirement 1]
- [Timeliness requirement 2]

## Access Patterns

### Common Queries
1. [Query description 1]
2. [Query description 2]
3. [Query description 3]

### Performance Requirements
- [Performance requirement 1]
- [Performance requirement 2]

## Data Governance

### Privacy
- [Privacy requirement 1]
- [Privacy requirement 2]

### Security
- [Security requirement 1]
- [Security requirement 2]

### Compliance
- [Compliance requirement 1]
- [Compliance requirement 2]

## Success Metrics
- [Success metric 1]
- [Success metric 2]
- [Success metric 3]
"""
    
    # Determine output path
    if output_path:
        file_path = output_path
    else:
        file_path = f"examples/{name.lower().replace(' ', '_')}_dda.md"
    
    # Create directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write template to file
    with open(file_path, 'w') as f:
        f.write(template_content)
    
    typer.echo(f"✅ DDA template created: {file_path}")
    typer.echo(f"📝 Template name: {name}")
    typer.echo(f"🔧 Next steps: Edit the template with domain-specific information")


if __name__ == "__main__":
    app()
