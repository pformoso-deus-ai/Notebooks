from typing import List, Dict, Optional
from domain.graph import GraphRepository, Node, Relationship


class InMemoryGraphRepository(GraphRepository):
    """Simple in-memory graph repository for development and testing."""

    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._relationships: Dict[str, List[Relationship]] = {}

    async def add_nodes(self, nodes: List[Node]) -> None:
        """Add nodes to the in-memory graph."""
        for node in nodes:
            self._nodes[node.id] = node

    async def add_relationships(self, relationships: List[Relationship]) -> None:
        """Add relationships to the in-memory graph."""
        for rel in relationships:
            if rel.source_id not in self._relationships:
                self._relationships[rel.source_id] = []
            self._relationships[rel.source_id].append(rel)

    async def get_node(self, node_id: str) -> Optional[Node]:
        """Retrieve a node by its ID from the in-memory graph."""
        return self._nodes.get(node_id)

    async def get_relationships(self, node_id: str) -> List[Relationship]:
        """Get all relationships for a given node from the in-memory graph."""
        return self._relationships.get(node_id, [])

    async def clear(self) -> None:
        """Clear all nodes and relationships from the repository."""
        self._nodes.clear()
        self._relationships.clear()
