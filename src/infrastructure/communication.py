from collections import defaultdict
from typing import Dict, List, Optional
import asyncio

from domain.communication import CommunicationChannel, Message


class InMemoryCommunicationChannel(CommunicationChannel):
    """
    An in-memory implementation of the communication channel for testing.

    It uses asyncio queues to simulate mailboxes for each agent.
    """

    def __init__(self):
        self._mailboxes: Dict[str, asyncio.Queue[Message]] = defaultdict(asyncio.Queue)

    async def send(self, message: Message) -> None:
        """Puts a message into the receiver's mailbox queue."""
        receiver_id = message.receiver_id
        await self._mailboxes[receiver_id].put(message)
        print(f"Message sent from {message.sender_id} to {receiver_id}.")

    async def receive(self, agent_id: str) -> Optional[Message]:
        """Retrieves a message from the agent's mailbox queue."""
        if agent_id in self._mailboxes and not self._mailboxes[agent_id].empty():
            message = await self._mailboxes[agent_id].get()
            print(f"Message received by {agent_id}.")
            return message
        return None

    async def get_all_messages(self, agent_id: str) -> List[Message]:
        """Retrieves all messages currently in the agent's mailbox."""
        messages = []
        if agent_id in self._mailboxes:
            while not self._mailboxes[agent_id].empty():
                messages.append(await self._mailboxes[agent_id].get())
        return messages
