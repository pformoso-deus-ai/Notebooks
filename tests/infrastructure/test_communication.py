import pytest
from domain.communication import Message
from infrastructure.communication import InMemoryCommunicationChannel

pytestmark = pytest.mark.asyncio


@pytest.fixture
def channel() -> InMemoryCommunicationChannel:
    """Provides an instance of the in-memory communication channel."""
    return InMemoryCommunicationChannel()


async def test_send_and_receive_message(channel: InMemoryCommunicationChannel):
    """Test that a sent message can be received by the correct agent."""
    # Arrange
    sender_id = "agent1"
    receiver_id = "agent2"
    content = {"task": "test"}
    message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)

    # Act
    await channel.send(message)
    received_message = await channel.receive(receiver_id)

    # Assert
    assert received_message is not None
    assert received_message.id == message.id
    assert received_message.sender_id == sender_id
    assert received_message.receiver_id == receiver_id
    assert received_message.content == content


async def test_receive_no_message(channel: InMemoryCommunicationChannel):
    """Test that receiving from an empty mailbox returns None."""
    # Arrange
    agent_id = "agent3"

    # Act
    received_message = await channel.receive(agent_id)

    # Assert
    assert received_message is None


async def test_get_all_messages(channel: InMemoryCommunicationChannel):
    """Test retrieving all messages for an agent."""
    # Arrange
    agent_id = "agent4"
    messages = [
        Message(sender_id="s1", receiver_id=agent_id, content="msg1"),
        Message(sender_id="s2", receiver_id=agent_id, content="msg2"),
    ]
    for msg in messages:
        await channel.send(msg)

    # Act
    retrieved_messages = await channel.get_all_messages(agent_id)

    # Assert
    assert len(retrieved_messages) == 2
    # Check that mailbox is now empty
    assert await channel.receive(agent_id) is None
