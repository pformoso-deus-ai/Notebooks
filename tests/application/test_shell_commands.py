import pytest
from application.commands.shell_commands import (
    ExecuteShellCommand,
    ExecuteShellCommandHandler,
    ShellCommandResult,
)

pytestmark = pytest.mark.asyncio


async def test_execute_shell_command_success():
    """
    Test that a successful shell command returns the correct output and exit code.
    """
    # Arrange
    handler = ExecuteShellCommandHandler()
    command = ExecuteShellCommand(command='echo "Success!"')

    # Act
    result = await handler.handle(command)

    # Assert
    assert isinstance(result, ShellCommandResult)
    assert result.return_code == 0
    assert result.stdout.strip() == "Success!"
    assert result.stderr == ""


async def test_execute_shell_command_failure():
    """
    Test that a failing shell command returns a non-zero exit code.
    """
    # Arrange
    handler = ExecuteShellCommandHandler()
    # Using a command that is likely to fail or produce stderr
    command = ExecuteShellCommand(command="ls non_existent_directory_12345")

    # Act
    result = await handler.handle(command)

    # Assert
    assert isinstance(result, ShellCommandResult)
    assert result.return_code != 0
    assert result.stderr != ""
