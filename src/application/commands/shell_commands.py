from dataclasses import dataclass
import subprocess
from .base import Command, CommandHandler


@dataclass
class ShellCommandResult:
    """The result of a shell command execution."""

    return_code: int
    stdout: str
    stderr: str


@dataclass
class ExecuteShellCommand(Command):
    """A command to execute a shell command."""

    command: str


class ExecuteShellCommandHandler(CommandHandler[ExecuteShellCommand]):
    """The handler for the ExecuteShellCommand."""

    async def handle(self, command: ExecuteShellCommand) -> ShellCommandResult:
        """
        Handles the ExecuteShellCommand by running it in a subprocess.

        Args:
            command: The ExecuteShellCommand instance.

        Returns:
            A ShellCommandResult containing the execution details.
        """
        print(f"Executing shell command: '{command.command}'")

        process = subprocess.run(
            command.command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,  # Do not raise exception on non-zero exit codes
        )

        result = ShellCommandResult(
            return_code=process.returncode, stdout=process.stdout, stderr=process.stderr
        )

        print(f"Shell command finished with return code: {result.return_code}")
        return result
