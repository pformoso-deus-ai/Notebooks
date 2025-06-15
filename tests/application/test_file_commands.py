import pytest
import tempfile
from pathlib import Path
from application.commands.file_commands import (
    CreateFileCommand,
    CreateFileCommandHandler,
    ReadFileCommand,
    ReadFileCommandHandler,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture
def temp_dir():
    """Create a temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


async def test_create_file_command_handler(temp_dir: Path):
    """
    Test that the CreateFileCommandHandler correctly creates a file
    with the specified content.
    """
    # Arrange
    handler = CreateFileCommandHandler()
    file_path = temp_dir / "test_dir" / "test_file.txt"
    content = "Hello from the test!"
    command = CreateFileCommand(path=str(file_path), content=content)

    # Act
    result = await handler.handle(command)

    # Assert
    assert file_path.exists()
    assert file_path.read_text() == content
    assert result == f"File created at: {file_path.resolve()}"


async def test_read_file_command_handler(temp_dir: Path):
    """
    Test that the ReadFileCommandHandler correctly reads content from a file.
    """
    # Arrange
    handler = ReadFileCommandHandler()
    file_path = temp_dir / "test_read.txt"
    content = "You are reading this."
    file_path.write_text(content)
    command = ReadFileCommand(path=str(file_path))

    # Act
    result = await handler.handle(command)

    # Assert
    assert result == content


async def test_read_nonexistent_file_raises_error(temp_dir: Path):
    """
    Test that reading a non-existent file returns an error message.
    """
    # Arrange
    handler = ReadFileCommandHandler()
    non_existent_path = temp_dir / "nonexistent.txt"
    command = ReadFileCommand(path=str(non_existent_path))

    # Act
    result = await handler.handle(command)

    # Assert
    assert "Error: File not found" in result
