from infrastructure.memory_graph import InMemoryGraphRepository
import pytest


def test_add_and_get_node():
    repo = InMemoryGraphRepository()
    node = {"id": "1", "value": "test"}
    repo.add_node(node)
    assert repo.get_node("1") == node


def test_add_node_missing_id_raises_value_error():
    repo = InMemoryGraphRepository()
    node = {"value": "no id"}
    with pytest.raises(ValueError):
        repo.add_node(node)
