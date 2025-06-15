from domain.agent import Agent
from application.commands.agent_commands import StartProjectCommand
from domain.graph import GraphTransformer
from domain.repositories import GraphRepository
from langchain_core.documents import Document


class EchoAgent(Agent):
    """
    A simple agent that echoes back any message it receives.
    """

    async def process_messages(self) -> None:
        """
        Continuously checks for messages and echoes them back.
        """
        print(f"[{self.agent_id}] Waiting for messages...")
        message = await self.receive_message()
        if message:
            print(f"[{self.agent_id}] Received message: {message.content}")
            # Echo the content back to the sender
            await self.send_message(
                receiver_id=message.sender_id, content=f"Echo: {message.content}"
            )
            print(f"[{self.agent_id}] Echoed message back to {message.sender_id}")


class ArxAgent(Agent):
    """
    The Architect agent (Arx).
    Focuses on high-level design and problem-solving.
    """

    def __init__(
        self,
        graph_repository: GraphRepository,
        graph_transformer: GraphTransformer,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.graph_repository = graph_repository
        self.graph_transformer = graph_transformer

    async def process_messages(self) -> None:
        """Processes incoming messages, looking for new project goals."""
        message = await self.receive_message()
        if not message:
            return

        if isinstance(message.content, StartProjectCommand):
            project_goal = message.content.project_goal
            print(f"[{self.agent_id}] Received new project goal: '{project_goal}'")

            # 1. Use transformer to create a plan.
            doc = Document(page_content=project_goal)
            graph_docs = await self.graph_transformer.transform([doc])

            if not graph_docs:
                print(f"[{self.agent_id}] Could not generate a plan from the goal.")
                return

            # For simplicity, we process the first graph document.
            plan_graph = graph_docs[0]

            # 2. Persist the plan to the graph repository.
            for node in plan_graph.nodes:
                await self.graph_repository.add_node(node)

            for rel in plan_graph.relationships:
                await self.graph_repository.add_relationship(rel)

            print(f"[{self.agent_id}] Plan created and saved to the graph.")
            print(f"  - Nodes created: {len(plan_graph.nodes)}")
            print(f"  - Relationships created: {len(plan_graph.relationships)}")

            # TODO: Send the first task to the DeveloperAgent.
        else:
            print(
                f"[{self.agent_id}] Received unhandled message type: {type(message.content)}"
            )


class DeveloperAgent(Agent):
    """
    The Developer agent (D).
    Handles implementation and can challenge design decisions.
    """

    async def process_messages(self) -> None:
        # Currently idle. Future logic will involve coding and execution tasks.
        pass
