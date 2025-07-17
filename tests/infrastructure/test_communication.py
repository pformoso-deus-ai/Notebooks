import pytest
from domain.communication import Message
from infrastructure.communication.memory_channel import InMemoryCommunicationChannel

@pytest.mark.asyncio
async def test_in_memory_communication_channel():
    # Arrange
    channel = InMemoryCommunicationChannel()
    agent1_id = "agent1"
    agent2_id = "agent2"
    message_to_agent1 = Message(
        sender_id=agent2_id,
        receiver_id=agent1_id,
        content="Hello Agent 1",
    )
    message_to_agent2 = Message(
        sender_id=agent1_id,
        receiver_id=agent2_id,
        content="Hi Agent 2",
    )

    # Act
    await channel.send(message_to_agent1)
    await channel.send(message_to_agent2)

    # Assert
    # Agent 1 receives their message
    received_msg1 = await channel.receive(agent1_id)
    assert received_msg1 is not None
    assert received_msg1.content == "Hello Agent 1"
    assert await channel.receive(agent1_id) is None  # No more messages

    # Agent 2 receives their message
    received_msg2 = await channel.receive(agent2_id)
    assert received_msg2 is not None
    assert received_msg2.content == "Hi Agent 2"
    assert await channel.receive(agent2_id) is None  # No more messages


@pytest.mark.asyncio
async def test_get_all_messages():
    # Arrange
    channel = InMemoryCommunicationChannel()
    agent_id = "test-agent"
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
    assert retrieved_messages[0].content == "msg1"
    assert retrieved_messages[1].content == "msg2"
    # Ensure the mailbox is now empty
    assert await channel.receive(agent_id) is None
