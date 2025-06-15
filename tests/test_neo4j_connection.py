import pytest
from neo4j import GraphDatabase
from langchain_community.graphs import Neo4jGraph

# Neo4j Aura connection details
USERNAME = "neo4j"
PASSWORD = "x83ShgOAEYvlhevv5Uici_D9CEIsVr8Neu-KEkGOLPo"

# Different connection string formats to try
CONNECTION_STRINGS = [
    "neo4j+s://112e8139.databases.neo4j.io",
    "neo4j+s://112e8139.databases.neo4j.io:7687",
    "bolt+s://112e8139.databases.neo4j.io:7687",
    "bolt://112e8139.databases.neo4j.io:7687",
]


def test_direct_neo4j_connection():
    """Test direct connection using Neo4j driver with different connection strings"""
    for uri in CONNECTION_STRINGS:
        try:
            print(f"\nTrying connection string: {uri}")
            driver = GraphDatabase.driver(uri, auth=(USERNAME, PASSWORD))
            # Verify connection
            with driver.session() as session:
                result = session.run("RETURN 1 as n")
                record = result.single()
                assert record["n"] == 1
            driver.close()
            print(f"Success! Connection string {uri} works!")
            return  # Exit on first successful connection
        except Exception as e:
            print(f"Failed with {uri}: {str(e)}")
            continue

    pytest.fail("All connection attempts failed")


def test_langchain_neo4j_connection():
    """Test connection using LangChain's Neo4jGraph"""
    for uri in CONNECTION_STRINGS:
        try:
            print(f"\nTrying LangChain connection with: {uri}")
            graph = Neo4jGraph(url=uri, username=USERNAME, password=PASSWORD)
            # Verify connection
            result = graph.query("RETURN 1 as n")
            assert result[0]["n"] == 1
            print(f"Success! LangChain connection with {uri} works!")
            return  # Exit on first successful connection
        except Exception as e:
            print(f"Failed with {uri}: {str(e)}")
            continue

    pytest.fail("All LangChain connection attempts failed")


if __name__ == "__main__":
    print("Testing Neo4j connections...")
    test_direct_neo4j_connection()
    test_langchain_neo4j_connection()
