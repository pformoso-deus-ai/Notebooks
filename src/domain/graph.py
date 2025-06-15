from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
from langchain_core.documents import Document


class NodeLabel(str, Enum):
    """Available node labels in the knowledge graph"""

    AGENT = "Agent"
    TASK = "Task"
    SOLUTION = "Solution"
    CONCEPT = "Concept"
    ARTIFACT = "Artifact"


class RelationshipType(str, Enum):
    """Available relationship types in the knowledge graph"""

    CREATES = "CREATES"
    IMPLEMENTS = "IMPLEMENTS"
    DEPENDS_ON = "DEPENDS_ON"
    DISCUSSES = "DISCUSSES"
    REFERENCES = "REFERENCES"
    MENTIONS = "MENTIONS"


@dataclass
class Node:
    """Represents a node in the knowledge graph"""

    id: str
    label: NodeLabel
    properties: Dict[str, Any]


@dataclass
class Relationship:
    """Represents a relationship in the knowledge graph"""

    source_id: str
    target_id: str
    type: RelationshipType
    properties: Dict[str, Any]


class GraphRepository(ABC):
    """Abstract interface for graph operations"""

    @abstractmethod
    async def add_nodes(self, nodes: List[Node]) -> None:
        """Add nodes to the graph"""
        pass

    @abstractmethod
    async def add_relationships(self, relationships: List[Relationship]) -> None:
        """Add relationships to the graph"""
        pass

    @abstractmethod
    async def get_node(self, node_id: str) -> Optional[Node]:
        """Retrieve a node by its ID"""
        pass

    @abstractmethod
    async def get_relationships(self, node_id: str) -> List[Relationship]:
        """Get all relationships for a given node"""
        pass


@dataclass
class GraphDocument:
    """A document represented as a graph."""

    nodes: List[Node]
    relationships: List[Relationship]
    source: Document


class GraphTransformer(ABC):
    """Abstract class for transforming text into a knowledge graph"""

    @abstractmethod
    async def transform(self, documents: List[Document]) -> List[GraphDocument]:
        """Transform a list of documents into a list of graph documents."""
        pass
