"""Neo4J graph repository implementation."""

from __future__ import annotations

from domain.repositories import GraphRepository

try:
    from neo4j import GraphDatabase
except Exception:  # pragma: no cover - fallback when neo4j is missing
    GraphDatabase = None  # type: ignore


class Neo4JGraphRepository(GraphRepository):
    """Repository backed by a Neo4J database."""

    def __init__(self, uri: str, user: str, password: str) -> None:
        if GraphDatabase is None:  # pragma: no cover - environment without neo4j
            raise ImportError("neo4j driver is not installed")
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        """Close the underlying Neo4J driver."""
        self._driver.close()

    # ------------------------------------------------------------------
    # GraphRepository API
    # ------------------------------------------------------------------
    def add_node(self, node: dict) -> None:  # pragma: no cover - placeholder
        """Persist a node using a Cypher query."""
        if GraphDatabase is None:
            raise NotImplementedError("neo4j driver is required for add_node")

        node_id = node.get("id")
        if not node_id:
            raise ValueError("node must have an 'id'")

        query = "MERGE (n {id: $id}) SET n += $props"
        with self._driver.session() as session:
            session.run(query, id=node_id, props=node)

    def get_node(self, node_id: str) -> dict:  # pragma: no cover - placeholder
        """Retrieve a node by id using a Cypher query."""
        if GraphDatabase is None:
            raise NotImplementedError("neo4j driver is required for get_node")

        query = "MATCH (n {id: $id}) RETURN properties(n) AS node"
        with self._driver.session() as session:
            result = session.run(query, id=node_id)
            record = result.single()
            if record is None:
                raise KeyError(node_id)
            return dict(record["node"])
