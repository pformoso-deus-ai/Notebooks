from infrastructure.memory_graph import InMemoryGraphRepository


def test_add_and_get_node():
    repo = InMemoryGraphRepository()
    node = {"id": "1", "value": "test"}
    repo.add_node(node)
    assert repo.get_node("1") == node
