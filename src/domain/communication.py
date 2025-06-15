from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class Message:
    """Represents a message passed between agents."""

    sender_id: str
    receiver_id: str
    content: Any
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)


class CommunicationChannel(ABC):
    """An abstract interface for agent-to-agent communication."""

    @abstractmethod
    async def send(self, message: Message) -> None:
        """
        Sends a message to a specific agent.

        Args:
            message: The message to send.
        """
        pass

    @abstractmethod
    async def receive(self, agent_id: str) -> Optional[Message]:
        """
        Receives a message for a specific agent.

        This can be a polling or a blocking call depending on the implementation.

        Args:
            agent_id: The ID of the agent to receive a message for.

        Returns:
            The received message, or None if no message is available.
        """
        pass

    @abstractmethod
    async def get_all_messages(self, agent_id: str) -> List[Message]:
        """
        Retrieves all messages for a specific agent.

        Args:
            agent_id: The ID of the agent.

        Returns:
            A list of all messages for the agent.
        """
        pass
