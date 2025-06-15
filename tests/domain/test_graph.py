from domain.graph import Node, Relationship, NodeLabel, RelationshipType


def test_node_creation():
    """Test node creation with valid data"""
    node = Node(id="test-1", label=NodeLabel.AGENT, properties={"name": "Test Agent"})
    assert node.id == "test-1"
    assert node.label == NodeLabel.AGENT
    assert node.properties == {"name": "Test Agent"}


def test_relationship_creation():
    """Test relationship creation with valid data"""
    rel = Relationship(
        source_id="agent-1",
        target_id="task-1",
        type=RelationshipType.CREATES,
        properties={"timestamp": "2024-02-20"},
    )
    assert rel.source_id == "agent-1"
    assert rel.target_id == "task-1"
    assert rel.type == RelationshipType.CREATES
    assert rel.properties == {"timestamp": "2024-02-20"}


def test_node_label_enum():
    """Test that node labels are properly defined"""
    assert NodeLabel.AGENT.value == "Agent"
    assert NodeLabel.TASK.value == "Task"
    assert NodeLabel.SOLUTION.value == "Solution"
    assert NodeLabel.CONCEPT.value == "Concept"
    assert NodeLabel.ARTIFACT.value == "Artifact"


def test_relationship_type_enum():
    """Test that relationship types are properly defined"""
    assert RelationshipType.CREATES.value == "CREATES"
    assert RelationshipType.IMPLEMENTS.value == "IMPLEMENTS"
    assert RelationshipType.DEPENDS_ON.value == "DEPENDS_ON"
    assert RelationshipType.DISCUSSES.value == "DISCUSSES"
    assert RelationshipType.REFERENCES.value == "REFERENCES"
