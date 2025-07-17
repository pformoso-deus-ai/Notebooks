import pytest
from application.commands.base import CommandBus
from application.commands.echo_command import EchoCommand, EchoCommandHandler

pytestmark = pytest.mark.asyncio


@pytest.fixture
def command_bus() -> CommandBus:
    """Fixture to create a CommandBus and register the EchoCommandHandler."""
    bus = CommandBus()
    bus.register(EchoCommand, EchoCommandHandler())
    return bus


async def test_command_bus_executes_handler(command_bus: CommandBus):
    """Test that the CommandBus correctly dispatches a command to its handler."""
    # Arrange
    command = EchoCommand(text="Hello, World!")

    # Act
    result = await command_bus.dispatch(command)

    # Assert
    assert result == "Hello, World!"


async def test_unregistered_command_raises_error(command_bus: CommandBus):
    """Test that executing an unregistered command raises a TypeError."""

    # Arrange
    class UnregisteredCommand(EchoCommand):
        pass

    command = UnregisteredCommand(text="This should fail.")

    # Act & Assert
    with pytest.raises(
        TypeError, match="No handler registered for command type UnregisteredCommand"
    ):
        await command_bus.dispatch(command)
