from domain.agent import Agent
from application.commands.agent_commands import StartProjectCommand
from graphiti.graph import Graph
from graphiti.llm import LLM
from langchain_core.documents import Document
from typing import Optional
from domain.communication import CommunicationChannel
from src.domain.command_bus import CommandBus


class DataArchitectAgent(Agent):
    """
    The Data Architect agent.
    Focuses on high-level design and problem-solving.
    """

    def __init__(
        self,
        agent_id: str,
        command_bus: CommandBus,
        communication_channel: CommunicationChannel,
        graph: Graph,
        llm: LLM,
        url: str,
    ):
        super().__init__(
            agent_id=agent_id,
            command_bus=command_bus,
            communication_channel=communication_channel,
        )
        self.graph = graph
        self.llm = llm
        self.url = url

    async def register_self(self):
        """
        Registers the agent as a service in the knowledge graph.
        """
        await self.graph.upsert_node(
            "AgentService",
            self.agent_id,
            {"url": self.url, "capabilities": ["design", "planning"]},
        )

    async def discover_agent(self, capability: str) -> Optional[str]:
        """
        Discovers an agent with a specific capability by querying the
        knowledge graph. Returns the agent's URL.
        """
        nodes = await self.graph.get_nodes(
            "AgentService", {"capability": capability}
        )
        if nodes:
            # For simplicity, return the first agent found
            return nodes[0].properties.get("url")
        return None

    async def process_messages(self) -> None:
        """Processes incoming messages, looking for new project goals."""
        message = await self.receive_message()
        if not message:
            return

        if isinstance(message.content, StartProjectCommand):
            project_goal = message.content.project_goal
            print(f"[{self.agent_id}] Received new project goal: '{project_goal}'")

            # 1. Use llm to create a plan.
            graph_document = self.llm.process(project_goal)
            
            # 2. Persist the plan to the graph.
            self.graph.add_graph_document(graph_document)
            
            print(f"[{self.agent_id}] Plan created and saved to the graph.")
            print(f"  - Nodes created: {len(graph_document.nodes)}")
            print(f"  - Relationships created: {len(graph_document.relationships)}")

            # TODO: Send the first task to the DataEngineerAgent.
        else:
            print(
                f"[{self.agent_id}] Received unhandled message type: {type(message.content)}"
            ) 