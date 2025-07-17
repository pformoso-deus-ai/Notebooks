from domain.agent import Agent
from domain.communication import CommunicationChannel
from src.domain.command_bus import CommandBus
from graphiti.graph import Graph
from typing import Optional


class DataEngineerAgent(Agent):
    """
    The Data Engineer agent.
    Handles implementation and can challenge design decisions.
    """

    def __init__(
        self,
        agent_id: str,
        command_bus: CommandBus,
        communication_channel: CommunicationChannel,
        graph: Graph,
        url: str,
    ):
        super().__init__(
            agent_id, command_bus, communication_channel
        )
        self.graph = graph
        self.url = url

    async def register_self(self):
        """
        Registers the agent as a service in the knowledge graph.
        """
        await self.graph.upsert_node(
            "AgentService",
            self.agent_id,
            {"url": self.url, "capabilities": ["implementation"]},
        )

    async def process_messages(self) -> None:
        # Currently idle. Future logic will involve coding and execution tasks.
        pass 