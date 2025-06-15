import pytest
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from domain.graph import Node, Relationship, NodeLabel, RelationshipType
from infrastructure.memory_graph import InMemoryGraphRepository
from infrastructure.neo4j_graph import Neo4JGraphRepository
from infrastructure.llm_graph_transformer import LangChainGraphTransformer

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-fake-key")


@pytest.fixture
def sample_node() -> Node:
    """Fixture providing a sample node for testing"""
    return Node(
        id="test-agent-1",
        label=NodeLabel.AGENT,
        properties={"name": "Test Agent", "role": "developer"},
    )


@pytest.fixture
def sample_relationship(sample_node) -> Relationship:
    """Fixture providing a sample relationship for testing"""
    return Relationship(
        source_id=sample_node.id,
        target_id="test-task-1",
        type=RelationshipType.CREATES,
        properties={"timestamp": "2024-02-20"},
    )


@pytest.fixture
async def memory_repository() -> AsyncGenerator[InMemoryGraphRepository, None]:
    """Fixture providing an in-memory graph repository for testing"""
    repo = InMemoryGraphRepository()
    yield repo
    # Cleanup if needed
    await repo.clear()


@pytest.fixture
async def neo4j_repository() -> AsyncGenerator[Neo4JGraphRepository, None]:
    """Fixture providing a Neo4j graph repository for testing"""
    repo = Neo4JGraphRepository(
        url=URI,
        username=USER,
        password=PASSWORD,
    )
    yield repo
    await repo.clear()


@pytest.fixture
def llm_transformer() -> LangChainGraphTransformer:
    """Fixture providing a LLM Graph Transformer for testing"""
    return LangChainGraphTransformer(
        neo4j_url=URI,
        neo4j_username=USER,
        neo4j_password=PASSWORD,
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4o-mini",
    )
