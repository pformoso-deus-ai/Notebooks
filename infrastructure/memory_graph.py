from typing import Dict

from domain.repositories import GraphRepository


class InMemoryGraphRepository(GraphRepository):
    """Simple in-memory graph repository used for development."""

    def __init__(self) -> None:
        self._nodes: Dict[str, dict] = {}

    def add_node(self, node: dict) -> None:
        node_id = node.get("id")
        if not node_id:
            raise ValueError("node must have an 'id'")
        self._nodes[node_id] = node

    def get_node(self, node_id: str) -> dict:
        return self._nodes[node_id]
