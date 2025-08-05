"""Tests for the Knowledge Manager Agent."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timezone
from application.agents.knowledge_manager.agent import (
    KnowledgeManagerAgent,
    KGUpdateRequest,
    KGUpdateType,
    KGUpdateResult
)
from domain.communication import Message
from domain.agent import Agent


class TestKnowledgeManagerAgent:
    """Test cases for KnowledgeManagerAgent."""
    
    @pytest.fixture
    def mock_graph(self):
        """Create a mock Graphiti instance."""
        mock = Mock()
        mock.add_episode = AsyncMock()
        mock.add_episode.return_value = Mock(
            episode=Mock(uuid="test-episode-uuid"),
            nodes=["node1", "node2"],
            edges=["edge1"]
        )
        return mock
    
    @pytest.fixture
    def knowledge_manager_agent(self, mock_graph):
        """Create a KnowledgeManagerAgent instance for testing."""
        return KnowledgeManagerAgent(graph=mock_graph, llm=mock_graph)
    
    @pytest.fixture
    def sample_kg_update_request(self):
        """Create a sample KG update request."""
        return KGUpdateRequest(
            update_type=KGUpdateType.COMPLEX_MERGE,
            source_agent="data_architect",
            domain="test_domain",
            entities=[
                {"name": "TestEntity1", "description": "Test entity 1"},
                {"name": "TestEntity2", "description": "Test entity 2"}
            ],
            relationships=[
                {"source": "TestEntity1", "target": "TestEntity2", "type": "relates_to"}
            ],
            metadata={"priority": "high", "source": "test"},
            priority=1
        )
    
    def test_agent_initialization(self, knowledge_manager_agent):
        """Test that the agent initializes correctly."""
        assert knowledge_manager_agent.name == "knowledge_manager"
        assert knowledge_manager_agent.description == "Handles complex KG operations and reasoning"
        assert knowledge_manager_agent.graph is not None
        assert knowledge_manager_agent.llm is not None
        assert knowledge_manager_agent._update_queue is not None
        assert knowledge_manager_agent._processing is False
        assert knowledge_manager_agent._audit_log == []
    
    @pytest.mark.asyncio
    async def test_agent_start_stop(self, knowledge_manager_agent):
        """Test agent start and stop functionality."""
        # Start the agent
        await knowledge_manager_agent.start()
        assert knowledge_manager_agent._processing is True
        
        # Stop the agent
        await knowledge_manager_agent.stop()
        assert knowledge_manager_agent._processing is False
    
    @pytest.mark.asyncio
    async def test_escalate_update_success(self, knowledge_manager_agent, sample_kg_update_request):
        """Test successful escalation of KG update."""
        result = await knowledge_manager_agent.escalate_update(sample_kg_update_request)
        
        assert isinstance(result, KGUpdateResult)
        assert result.success is True
        assert result.request_id == sample_kg_update_request.request_id
        assert result.nodes_created == 2
        assert result.edges_created == 1
        assert result.conflicts_resolved == 0
        assert result.validation_errors == []
        assert result.rollback_performed is False
        assert result.error_message is None
        
        # Check audit log
        audit_log = knowledge_manager_agent.get_audit_log()
        assert len(audit_log) == 1
        assert audit_log[0]["request_id"] == sample_kg_update_request.request_id
        assert audit_log[0]["source_agent"] == "data_architect"
        assert audit_log[0]["update_type"] == "complex_merge"
        assert audit_log[0]["success"] is True
    
    @pytest.mark.asyncio
    async def test_escalate_update_validation_failure(self, knowledge_manager_agent):
        """Test escalation with validation failure."""
        # Create request with missing required fields
        invalid_request = KGUpdateRequest(
            update_type=KGUpdateType.VALIDATION_FAILURE,
            source_agent="data_architect",
            domain="",  # Empty domain should fail validation
            entities=[],
            relationships=[],
            metadata={}
        )
        
        result = await knowledge_manager_agent.escalate_update(invalid_request)
        
        assert isinstance(result, KGUpdateResult)
        assert result.success is False
        assert "Domain is required" in result.validation_errors
        assert "At least entities or relationships must be provided" in result.validation_errors
    
    @pytest.mark.asyncio
    async def test_escalate_update_entity_validation_failure(self, knowledge_manager_agent):
        """Test escalation with entity validation failure."""
        invalid_request = KGUpdateRequest(
            update_type=KGUpdateType.VALIDATION_FAILURE,
            source_agent="data_architect",
            domain="test_domain",
            entities=[{"description": "Missing name"}],  # Missing name
            relationships=[],
            metadata={}
        )
        
        result = await knowledge_manager_agent.escalate_update(invalid_request)
        
        assert isinstance(result, KGUpdateResult)
        assert result.success is False
        assert "Entity name is required" in result.validation_errors
    
    @pytest.mark.asyncio
    async def test_escalate_update_relationship_validation_failure(self, knowledge_manager_agent):
        """Test escalation with relationship validation failure."""
        invalid_request = KGUpdateRequest(
            update_type=KGUpdateType.VALIDATION_FAILURE,
            source_agent="data_architect",
            domain="test_domain",
            entities=[],
            relationships=[{"type": "invalid"}],  # Missing source and target
            metadata={}
        )
        
        result = await knowledge_manager_agent.escalate_update(invalid_request)
        
        assert isinstance(result, KGUpdateResult)
        assert result.success is False
        assert "Relationship source and target are required" in result.validation_errors
    
    @pytest.mark.asyncio
    async def test_process_message_kg_update_request(self, knowledge_manager_agent):
        """Test processing KG update request message."""
        message = Message(
            sender_id="data_architect",
            receiver_id="knowledge_manager",
            content={
                "type": "kg_update_request",
                "update_type": "complex_merge",
                "source_agent": "data_architect",
                "domain": "test_domain",
                "entities": [{"name": "TestEntity", "description": "Test"}],
                "relationships": [],
                "metadata": {},
                "priority": 1
            }
        )
        
        response = await knowledge_manager_agent.process_message(message)
        
        assert response.sender_id == "knowledge_manager"
        assert response.receiver_id == "data_architect"
        assert response.content["type"] == "kg_update_response"
        assert response.content["success"] is True
    
    @pytest.mark.asyncio
    async def test_process_message_kg_query(self, knowledge_manager_agent):
        """Test processing KG query message."""
        message = Message(
            sender_id="data_architect",
            receiver_id="knowledge_manager",
            content={
                "type": "kg_query",
                "domain": "test_domain",
                "query_type": "entities",
                "filters": {}
            }
        )
        
        response = await knowledge_manager_agent.process_message(message)
        
        assert response.sender_id == "knowledge_manager"
        assert response.receiver_id == "data_architect"
        assert response.content["type"] == "kg_query_response"
    
    @pytest.mark.asyncio
    async def test_process_message_validation_request(self, knowledge_manager_agent):
        """Test processing validation request message."""
        message = Message(
            sender_id="data_architect",
            receiver_id="knowledge_manager",
            content={
                "type": "validation_request",
                "domain": "test_domain",
                "entities": [{"name": "TestEntity", "description": "Test"}],
                "relationships": []
            }
        )
        
        response = await knowledge_manager_agent.process_message(message)
        
        assert response.sender_id == "knowledge_manager"
        assert response.receiver_id == "data_architect"
        assert response.content["type"] == "validation_response"
        assert response.content["valid"] is True
    
    @pytest.mark.asyncio
    async def test_process_message_unknown_type(self, knowledge_manager_agent):
        """Test processing unknown message type."""
        message = Message(
            sender_id="data_architect",
            receiver_id="knowledge_manager",
            content={"type": "unknown_type"}
        )
        
        response = await knowledge_manager_agent.process_message(message)
        
        assert response.sender_id == "knowledge_manager"
        assert response.receiver_id == "data_architect"
        assert "error" in response.content
        assert response.content["error"] == "Unknown message type"
    
    @pytest.mark.asyncio
    async def test_process_message_exception_handling(self, knowledge_manager_agent):
        """Test exception handling in message processing."""
        message = Message(
            sender_id="data_architect",
            receiver_id="knowledge_manager",
            content={"type": "kg_update_request", "invalid": "data"}
        )
    
        response = await knowledge_manager_agent.process_message(message)
    
        assert response.sender_id == "knowledge_manager"
        assert response.receiver_id == "data_architect"
        assert "error_message" in response.content
    
    @pytest.mark.asyncio
    async def test_escalate_update_exception_handling(self, knowledge_manager_agent):
        """Test exception handling in escalate update."""
        # Mock graph to raise exception
        knowledge_manager_agent.graph.add_episode.side_effect = Exception("Test error")
        
        sample_request = KGUpdateRequest(
            update_type=KGUpdateType.COMPLEX_MERGE,
            source_agent="data_architect",
            domain="test_domain",
            entities=[{"name": "TestEntity", "description": "Test"}],
            relationships=[],
            metadata={}
        )
        
        result = await knowledge_manager_agent.escalate_update(sample_request)
        
        assert isinstance(result, KGUpdateResult)
        assert result.success is False
        assert result.error_message == "Test error"
        assert result.rollback_performed is True
    
    def test_get_audit_log(self, knowledge_manager_agent):
        """Test getting audit log."""
        # Add some test audit entries
        knowledge_manager_agent._audit_log = [
            {
                "timestamp": datetime.now(timezone.utc),
                "request_id": "test_request_1",
                "source_agent": "data_architect",
                "update_type": "complex_merge",
                "success": True,
                "nodes_created": 2,
                "edges_created": 1
            },
            {
                "timestamp": datetime.now(timezone.utc),
                "request_id": "test_request_2",
                "source_agent": "data_engineer",
                "update_type": "conflict_resolution",
                "success": False,
                "nodes_created": 0,
                "edges_created": 0
            }
        ]
        
        audit_log = knowledge_manager_agent.get_audit_log()
        
        assert len(audit_log) == 2
        assert audit_log[0]["request_id"] == "test_request_1"
        assert audit_log[1]["request_id"] == "test_request_2"
        assert audit_log[0]["success"] is True
        assert audit_log[1]["success"] is False
    
    def test_kg_update_request_creation(self, sample_kg_update_request):
        """Test KGUpdateRequest creation and properties."""
        assert sample_kg_update_request.update_type == KGUpdateType.COMPLEX_MERGE
        assert sample_kg_update_request.source_agent == "data_architect"
        assert sample_kg_update_request.domain == "test_domain"
        assert len(sample_kg_update_request.entities) == 2
        assert len(sample_kg_update_request.relationships) == 1
        assert sample_kg_update_request.metadata["priority"] == "high"
        assert sample_kg_update_request.priority == 1
        assert sample_kg_update_request.timestamp is not None
        assert sample_kg_update_request.request_id.startswith("complex_merge_test_domain_")
    
    def test_kg_update_result_creation(self):
        """Test KGUpdateResult creation and properties."""
        result = KGUpdateResult(
            success=True,
            request_id="test_request_123",
            nodes_created=5,
            edges_created=3,
            conflicts_resolved=2,
            validation_errors=["error1"],
            reasoning_applied=["rule1", "rule2"],
            rollback_performed=False,
            error_message=None
        )
        
        assert result.success is True
        assert result.request_id == "test_request_123"
        assert result.nodes_created == 5
        assert result.edges_created == 3
        assert result.conflicts_resolved == 2
        assert result.validation_errors == ["error1"]
        assert result.reasoning_applied == ["rule1", "rule2"]
        assert result.rollback_performed is False
        assert result.error_message is None
        assert result.timestamp is not None
    
    @pytest.mark.asyncio
    async def test_update_queue_processing(self, knowledge_manager_agent):
        """Test that updates are properly queued and processed."""
        await knowledge_manager_agent.start()
        
        # Test that the queue can accept items
        sample_request = KGUpdateRequest(
            update_type=KGUpdateType.BATCH_UPDATE,
            source_agent="data_architect",
            domain="test_domain",
            entities=[{"name": "TestEntity", "description": "Test"}],
            relationships=[],
            metadata={}
        )
        
        # Test that we can put items in the queue
        await knowledge_manager_agent._update_queue.put(sample_request)
        
        # Test that the queue has the item
        assert not knowledge_manager_agent._update_queue.empty()
        
        # Test that we can get the item from the queue
        retrieved_request = await knowledge_manager_agent._update_queue.get()
        assert retrieved_request.request_id == sample_request.request_id
        
        await knowledge_manager_agent.stop()
    
    def test_kg_update_type_enum(self):
        """Test KGUpdateType enum values."""
        assert KGUpdateType.COMPLEX_MERGE.value == "complex_merge"
        assert KGUpdateType.CONFLICT_RESOLUTION.value == "conflict_resolution"
        assert KGUpdateType.VALIDATION_FAILURE.value == "validation_failure"
        assert KGUpdateType.REASONING_REQUIRED.value == "reasoning_required"
        assert KGUpdateType.BATCH_UPDATE.value == "batch_update"
        assert KGUpdateType.ONTOLOGY_UPDATE.value == "ontology_update" 