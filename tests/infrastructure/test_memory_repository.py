import pytest

pytestmark = pytest.mark.asyncio


async def test_add_and_get_node(memory_repository, sample_node):
    """Test adding and retrieving a node"""
    # Add node
    await memory_repository.add_nodes([sample_node])

    # Get node
    retrieved_node = await memory_repository.get_node(sample_node.id)
    assert retrieved_node is not None
    assert retrieved_node.id == sample_node.id
    assert retrieved_node.label == sample_node.label
    assert retrieved_node.properties == sample_node.properties


async def test_add_and_get_relationships(
    memory_repository, sample_node, sample_relationship
):
    """Test adding and retrieving relationships"""
    # Add node and relationship
    await memory_repository.add_nodes([sample_node])
    await memory_repository.add_relationships([sample_relationship])

    # Get relationships
    relationships = await memory_repository.get_relationships(sample_node.id)
    assert len(relationships) == 1
    assert relationships[0].source_id == sample_relationship.source_id
    assert relationships[0].target_id == sample_relationship.target_id
    assert relationships[0].type == sample_relationship.type
    assert relationships[0].properties == sample_relationship.properties


async def test_get_nonexistent_node(memory_repository):
    """Test retrieving a node that doesn't exist"""
    node = await memory_repository.get_node("nonexistent")
    assert node is None


async def test_get_relationships_for_nonexistent_node(memory_repository):
    """Test retrieving relationships for a node that doesn't exist"""
    relationships = await memory_repository.get_relationships("nonexistent")
    assert len(relationships) == 0


async def test_clear_repository(memory_repository, sample_node, sample_relationship):
    """Test clearing the repository"""
    # Add data
    await memory_repository.add_nodes([sample_node])
    await memory_repository.add_relationships([sample_relationship])

    # Clear
    await memory_repository.clear()

    # Verify data is gone
    node = await memory_repository.get_node(sample_node.id)
    assert node is None

    relationships = await memory_repository.get_relationships(sample_node.id)
    assert len(relationships) == 0
