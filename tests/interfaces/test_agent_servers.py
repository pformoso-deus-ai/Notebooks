import pytest
from fastapi.testclient import TestClient

from src.application.agents.data_engineer.server import create_app as create_data_engineer_app
from src.application.agents.data_architect.server import create_app as create_data_architect_app
from src.application.commands.base import CommandBus
from src.application.commands.collaboration_commands import BuildKGCommand
from src.application.agents.data_engineer.handlers.build_kg import BuildKGCommandHandler
from src.domain.agent_definition import AgentDefinition


@pytest.fixture
def data_engineer_client() -> TestClient:
    """Creates a test client for the Data Engineer agent's server."""
    command_bus = CommandBus()
    command_bus.register(BuildKGCommand, BuildKGCommandHandler())
    app = create_data_engineer_app(command_bus)
    return TestClient(app)


def test_data_engineer_agent_json_endpoint(data_engineer_client: TestClient):
    """
    Test that the Data Engineer's /.well-known/agent.json endpoint
    returns a valid AgentDefinition.
    """
    response = data_engineer_client.get("/.well-known/agent.json")
    assert response.status_code == 200

    # Validate the response against the Pydantic model
    agent_def = AgentDefinition(**response.json())

    assert agent_def.name == "Data Engineer Agent"
    assert len(agent_def.tools) == 1
    assert agent_def.tools[0].name == "BuildKGCommand"
    assert "metadata_uri" in agent_def.tools[0].parameters["properties"]


@pytest.fixture
def data_architect_client() -> TestClient:
    """Creates a test client for the Data Architect agent's server."""
    command_bus = CommandBus()
    # No commands registered by default for the architect
    app = create_data_architect_app(command_bus)
    return TestClient(app)


def test_data_architect_agent_json_endpoint(data_architect_client: TestClient):
    """
    Test that the Data Architect's /.well-known/agent.json endpoint
    returns a valid AgentDefinition with no tools.
    """
    response = data_architect_client.get("/.well-known/agent.json")
    assert response.status_code == 200

    agent_def = AgentDefinition(**response.json())

    assert agent_def.name == "Data Architect Agent"
    assert len(agent_def.tools) == 0 