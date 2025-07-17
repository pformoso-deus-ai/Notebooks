import pytest
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph
import os
from dotenv import load_dotenv

load_dotenv()

# Database credentials
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


@pytest.mark.integration
def test_raw_driver_connection():
    """Test raw driver connection to Neo4j."""
    pass # This test is a placeholder for now

@pytest.mark.integration
def test_langchain_neo4j_connection():
    """
    Test the connection to a Neo4j instance using the official library.
    This test requires a running Neo4j database.
    """
    try:
        graph = Neo4jGraph(url=URI, username=USERNAME, password=PASSWORD)
        # A simple query to verify the connection.
        result = graph.query("RETURN 1 AS number")
        assert result[0]["number"] == 1
    except Exception as e:
        pytest.fail(f"Neo4j connection test failed: {e}")


if __name__ == "__main__":
    print("Testing Neo4j connections...")
    test_raw_driver_connection()
    test_langchain_neo4j_connection()
