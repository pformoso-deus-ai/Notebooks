"""Placeholder FalkorDB backend implementation.

FalkorDB is a lightweight open-source graph database.  Similar to the
Graphiti stub, this class exists to satisfy the ``KnowledgeGraphBackend``
interface and signal where integration code should live.  All methods
raise ``NotImplementedError`` because no external connectivity is
available in this environment.
"""

from typing import Any, Dict

from domain.kg_backends import KnowledgeGraphBackend


class FalkorBackend(KnowledgeGraphBackend):
    """Stubbed backend for FalkorDB."""

    async def add_entity(self, entity_id: str, properties: Dict[str, Any]) -> None:
        raise NotImplementedError("FalkorDB backend integration not implemented")

    async def add_relationship(
        self,
        source_id: str,
        relationship_type: str,
        target_id: str,
        properties: Dict[str, Any],
    ) -> None:
        raise NotImplementedError("FalkorDB backend integration not implemented")

    async def rollback(self) -> None:
        raise NotImplementedError("FalkorDB backend integration not implemented")

    async def query(self, query: str) -> Any:
        raise NotImplementedError("FalkorDB backend integration not implemented")
