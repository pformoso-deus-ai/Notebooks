import pytest
from unittest.mock import AsyncMock, MagicMock
from application.agents.echo_agent import EchoAgent
from domain.communication import Message

@pytest.mark.asyncio
async def test_echo_agent_processes_message_and_sends_echo():
    # Arrange
    agent_id = "echo-1"
    sender_id = "test-sender"
    content = "Hello, Echo!"

    mock_channel = AsyncMock()
    mock_channel.receive.return_value = Message(
        sender_id=sender_id,
        receiver_id=agent_id,
        content=content,
    )

    agent = EchoAgent(
        agent_id=agent_id,
        command_bus=MagicMock(),
        communication_channel=mock_channel,
        url="http://localhost:8000",
    )

    # Act
    await agent.process_messages()

    # Assert
    # Check that receive was called
    mock_channel.receive.assert_awaited_once_with(agent_id)

    # Check that send was called with the echo message
    mock_channel.send.assert_awaited_once()
    sent_message = mock_channel.send.call_args[0][0]
    assert sent_message.receiver_id == sender_id
    assert sent_message.content == f"Echo: {content}"
