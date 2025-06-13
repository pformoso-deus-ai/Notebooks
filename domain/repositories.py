from abc import ABC, abstractmethod


class GraphRepository(ABC):
    """Abstract repository for graph operations."""

    @abstractmethod
    def add_node(self, node: dict) -> None:
        """Persist a node to the graph store."""

    @abstractmethod
    def get_node(self, node_id: str) -> dict:
        """Retrieve a node by its identifier."""
