import pytest

from application.agents import EchoAgent
from application.commands.base import CommandBus
from domain.communication import Message
from infrastructure.communication import InMemoryCommunicationChannel

pytestmark = pytest.mark.asyncio


@pytest.fixture
def command_bus() -> CommandBus:
    return CommandBus()


@pytest.fixture
def communication_channel() -> InMemoryCommunicationChannel:
    return InMemoryCommunicationChannel()


async def test_echo_agent_replies_to_message(
    command_bus: CommandBus, communication_channel: InMemoryCommunicationChannel
):
    """
    Test that the EchoAgent receives a message and sends a correct reply.
    """
    # Arrange
    initiator_id = "initiator_agent"
    echo_agent_id = "echo_agent"

    echo_agent = EchoAgent(
        agent_id=echo_agent_id,
        command_bus=command_bus,
        communication_channel=communication_channel,
    )

    original_content = "Hello, Echo!"
    initial_message = Message(
        sender_id=initiator_id,
        receiver_id=echo_agent_id,
        content=original_content,
    )

    # Act
    # 1. Initiator sends a message to the EchoAgent
    await communication_channel.send(initial_message)

    # 2. EchoAgent processes its messages
    await echo_agent.process_messages()

    # 3. Initiator checks for a reply
    reply_message = await communication_channel.receive(initiator_id)

    # Assert
    assert reply_message is not None
    assert reply_message.sender_id == echo_agent_id
    assert reply_message.receiver_id == initiator_id
    assert reply_message.content == f"Echo: {original_content}"
