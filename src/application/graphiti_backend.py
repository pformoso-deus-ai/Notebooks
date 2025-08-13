"""Placeholder Graphiti backend implementation.

Graphiti is an external knowledge graph platform.  Integrating with it
requires network access and authentication which are not available in
offline unit tests.  This stub serves to illustrate where such an
implementation would reside.  Attempting to use these methods will
raise ``NotImplementedError``.
"""

from typing import Any, Dict

from domain.kg_backends import KnowledgeGraphBackend


class GraphitiBackend(KnowledgeGraphBackend):
    """Stubbed backend for Graphiti.

    This class documents the methods required by the abstract interface.
    Real implementations should make HTTP requests to the Graphiti API
    to create nodes and relationships, handle errors, and support
    queries.  For brevity, all methods here simply raise
    ``NotImplementedError``.
    """

    async def add_entity(self, entity_id: str, properties: Dict[str, Any]) -> None:
        raise NotImplementedError("Graphiti backend integration not implemented")

    async def add_relationship(
        self,
        source_id: str,
        relationship_type: str,
        target_id: str,
        properties: Dict[str, Any],
    ) -> None:
        raise NotImplementedError("Graphiti backend integration not implemented")

    async def rollback(self) -> None:
        raise NotImplementedError("Graphiti backend integration not implemented")

    async def query(self, query: str) -> Any:
        raise NotImplementedError("Graphiti backend integration not implemented")