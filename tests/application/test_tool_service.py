from pydantic import BaseModel
import pytest
from src.application.services.tool_service import command_to_tool_definition
from src.domain.commands import Command


class SimpleCommand(Command, BaseModel):
    """A simple command for testing."""
    text: str
    number: int

def test_command_to_tool_definition():
    """Test that a Command is correctly converted to a ToolDefinition."""
    tool_def = command_to_tool_definition(SimpleCommand)

    assert tool_def.name == "SimpleCommand"
    assert tool_def.description == "A simple command for testing."
    assert tool_def.parameters["type"] == "object"
    assert "text" in tool_def.parameters["properties"]
    assert tool_def.parameters["properties"]["text"]["type"] == "string"
    assert "number" in tool_def.parameters["properties"]
    assert tool_def.parameters["properties"]["number"]["type"] == "integer"
    assert "text" in tool_def.parameters["required"]
    assert "number" in tool_def.parameters["required"]

def test_command_to_tool_definition_not_a_pydantic_model():
    """Test that a non-Pydantic Command raises a TypeError."""
    class NotAPydanticModelCommand(Command):
        pass

    with pytest.raises(TypeError, match="Command must be a Pydantic model."):
        command_to_tool_definition(NotAPydanticModelCommand) 