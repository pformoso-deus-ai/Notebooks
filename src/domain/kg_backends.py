"""Abstract interface for knowledge graph backends.

A knowledge graph backend is responsible for persisting entities and
relationships and providing a query interface.  Concrete implementations
should reside in the infrastructure layer.  By depending only on this
interface the application layer remains decoupled from specific database
technologies or services.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class KnowledgeGraphBackend(ABC):
    """Abstract base class for knowledge graph backends.

    Concrete implementations must implement all abstract methods defined
    here.  The asynchronous signatures allow backends to interact with
    remote services without blocking the event loop.
    """

    @abstractmethod
    async def add_entity(self, entity_id: str, properties: Dict[str, Any]) -> None:
        """Add an entity to the graph.

        Args:
            entity_id: A unique identifier for the node.
            properties: A mapping of property names to values.
        """
        raise NotImplementedError

    @abstractmethod
    async def add_relationship(
        self,
        source_id: str,
        relationship_type: str,
        target_id: str,
        properties: Dict[str, Any],
    ) -> None:
        """Add a relationship between two entities.

        Args:
            source_id: The identifier of the source node.
            relationship_type: The type/name of the relationship.
            target_id: The identifier of the target node.
            properties: A mapping of property names to values for the relationship.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the last operation.

        Implementations may maintain their own history stack to support
        rollback.  If rollback is unsupported the method should still
        exist but may simply raise ``NotImplementedError``.
        """
        raise NotImplementedError

    @abstractmethod
    async def query(self, query: str) -> Any:
        """Execute a query against the backend.

        The query string format is left unspecified because it depends
        on the underlying technology.  Simple implementations may ignore
        this parameter entirely and return internal state for testing.

        Args:
            query: A string representing the query.

        Returns:
            An arbitrary result.
        """
        raise NotImplementedError
