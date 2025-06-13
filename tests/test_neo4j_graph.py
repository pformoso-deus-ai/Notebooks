from infrastructure.neo4j_graph import Neo4JGraphRepository
import pytest
from unittest.mock import MagicMock


def _setup_repo(monkeypatch):
    mock_session = MagicMock()
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session

    mock_graph_db = MagicMock()
    mock_graph_db.driver.return_value = mock_driver
    monkeypatch.setattr(
        "infrastructure.neo4j_graph.GraphDatabase", mock_graph_db, raising=False
    )

    repo = Neo4JGraphRepository("bolt://localhost:7687", "user", "pass")
    return repo, mock_session


def test_add_and_get_node(monkeypatch):
    repo, session = _setup_repo(monkeypatch)
    node = {"id": "1", "value": "test"}

    repo.add_node(node)
    session.run.assert_called_with(
        "MERGE (n {id: $id}) SET n += $props", id="1", props=node
    )

    result = MagicMock()
    result.single.return_value = {"node": node}
    session.run.return_value = result

    assert repo.get_node("1") == node
    session.run.assert_called_with(
        "MATCH (n {id: $id}) RETURN properties(n) AS node", id="1"
    )


def test_add_node_missing_id_raises_value_error(monkeypatch):
    repo, _ = _setup_repo(monkeypatch)
    with pytest.raises(ValueError):
        repo.add_node({"value": "no id"})
