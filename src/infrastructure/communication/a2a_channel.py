from typing import List, Optional
import httpx

from domain.communication import CommunicationChannel, Message


class A2ACommunicationChannel(CommunicationChannel):
    """
    An implementation of the communication channel using the Google A2A protocol.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def send(self, message: Message) -> None:
        """Sends a message to another agent via an HTTP POST request."""
        # This is a simplified version. A full implementation would need to
        # map the domain Message to the A2A Task format.
        try:
            response = await self.client.post(
                f"{self.base_url}/v1/tasks/send",
                json={
                    "taskId": message.id,
                    "message": {
                        "role": "user",  # This needs more sophisticated mapping
                        "parts": [{"text": message.content}],
                    },
                },
            )
            response.raise_for_status()
            print(f"Message sent to {self.base_url} and received status {response.status_code}")
        except httpx.HTTPStatusError as e:
            print(f"Error sending message: {e.response.status_code} - {e.response.text}")

    async def receive(self, agent_id: str) -> Optional[Message]:
        """
        Receiving messages in A2A is handled by the server endpoint.
        This client-side method is not used for polling in a webhook-based system.
        It could be adapted for a polling mechanism if needed.
        """
        # In a true A2A model, the agent's server receives messages,
        # so a client-side receive might not be applicable.
        print("Receive method not implemented for A2A client-side channel.")
        return None

    async def get_all_messages(self, agent_id: str) -> List[Message]:
        """
        This method is not applicable for a client-side A2A channel.
        """
        print("get_all_messages method not implemented for A2A client-side channel.")
        return [] 