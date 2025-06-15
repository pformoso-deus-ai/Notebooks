from typing import List, Optional
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI

from domain.graph import (
    GraphDocument,
    GraphTransformer,
    Node,
    Relationship,
    NodeLabel,
    RelationshipType,
)


class LangChainGraphTransformer(GraphTransformer):
    """Adapter for LangChain's LLMGraphTransformer that converts text into a knowledge graph"""

    def __init__(
        self,
        neo4j_url: str,
        neo4j_username: str,
        neo4j_password: str,
        openai_api_key: str,
        model_name: str = "gpt-4-turbo-preview",
        temperature: float = 0,
        node_properties: Optional[List[str]] = None,
        include_source: bool = True,
        base_entity_label: bool = True,
    ):
        """Initialize the transformer with Neo4j connection and LLM settings

        Args:
            neo4j_url: URL for Neo4j database
            neo4j_username: Neo4j username
            neo4j_password: Neo4j password
            openai_api_key: OpenAI API key
            model_name: Name of the OpenAI model to use
            temperature: Temperature for the LLM (0 for deterministic)
            node_properties: List of properties to extract for nodes
            include_source: Whether to include source document relationships
            base_entity_label: Whether to add a base entity label to nodes
        """
        self.graph = Neo4jGraph(
            url=neo4j_url, username=neo4j_username, password=neo4j_password
        )

        self.llm = ChatOpenAI(
            api_key=openai_api_key, model_name=model_name, temperature=temperature
        )

        self.allowed_nodes = [label.value for label in NodeLabel]
        # Relationship directions are important for extraction
        self.allowed_relationships = [
            (
                NodeLabel.AGENT.value,
                RelationshipType.CREATES.value,
                NodeLabel.TASK.value,
            ),
            (
                NodeLabel.TASK.value,
                RelationshipType.DEPENDS_ON.value,
                NodeLabel.CONCEPT.value,
            ),
            (
                NodeLabel.AGENT.value,
                RelationshipType.IMPLEMENTS.value,
                NodeLabel.SOLUTION.value,
            ),
            (
                NodeLabel.AGENT.value,
                RelationshipType.DISCUSSES.value,
                NodeLabel.CONCEPT.value,
            ),
            (
                NodeLabel.ARTIFACT.value,
                RelationshipType.REFERENCES.value,
                NodeLabel.CONCEPT.value,
            ),
            (
                NodeLabel.AGENT.value,
                RelationshipType.MENTIONS.value,
                NodeLabel.TASK.value,
            ),
        ]

        self.transformer = LLMGraphTransformer(
            llm=self.llm,
            allowed_nodes=self.allowed_nodes,
            allowed_relationships=self.allowed_relationships,
            node_properties=node_properties,
            strict_mode=True,
        )

        self.include_source = include_source
        self.base_entity_label = base_entity_label

    async def transform(self, documents: List[Document]) -> List[GraphDocument]:
        """
        Transforms a list of documents into a list of GraphDocument objects.
        Filters out empty or whitespace-only documents before processing.
        """
        if not documents:
            return []

        # Filter out empty documents to avoid unnecessary API calls
        valid_documents = [doc for doc in documents if doc.page_content and doc.page_content.strip()]
        
        if not valid_documents:
            # Return a list of empty GraphDocument objects, one for each original empty document
            return [GraphDocument(nodes=[], relationships=[], source=doc) for doc in documents]

        # Use the underlying LangChain transformer
        langchain_graph_docs = await self.transformer.aconvert_to_graph_documents(
            valid_documents
        )

        # Here we could also persist to Neo4j if we wanted, but for now
        # the interface contract is just to transform.
        # self.graph.add_graph_documents(...)

        # Convert to our domain's GraphDocument
        domain_graph_docs: List[GraphDocument] = []
        for doc in langchain_graph_docs:
            nodes = [
                Node(
                    id=node.id,
                    label=NodeLabel(node.type),
                    properties=node.properties or {},
                )
                for node in doc.nodes
            ]
            relationships = [
                Relationship(
                    source_id=rel.source.id,
                    target_id=rel.target.id,
                    type=RelationshipType(rel.type),
                    properties=rel.properties or {},
                )
                for rel in doc.relationships
            ]
            domain_graph_docs.append(
                GraphDocument(
                    nodes=nodes, relationships=relationships, source=doc.source
                )
            )

        return domain_graph_docs
