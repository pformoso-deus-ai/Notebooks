import pytest
from unittest.mock import Mock, AsyncMock
from application.commands.modeling_command import ModelingCommand
from application.commands.modeling_handler import ModelingCommandHandler
from application.agents.data_architect.modeling_workflow import ModelingWorkflow, ModelingResult
from application.agents.data_architect.dda_parser import DDAParserFactory
from domain.dda_models import DDADocument, DataEntity, Relationship
from datetime import datetime
import tempfile
import os


class TestModelingCommandBasic:
    """Basic test cases for ModelingCommand without Graphiti dependencies."""
    
    def test_valid_command_creation(self):
        """Test creating a valid modeling command."""
        command = ModelingCommand(
            dda_path="examples/sample_dda.md",
            domain="Customer Analytics"
        )
        
        assert command.dda_path == "examples/sample_dda.md"
        assert command.domain == "Customer Analytics"
        assert command.update_existing is False
        assert command.validate_only is False
        assert command.output_path is None
    
    def test_command_with_nonexistent_file(self):
        """Test that command validation fails for nonexistent files."""
        with pytest.raises(ValueError, match="DDA file not found"):
            ModelingCommand(
                dda_path="nonexistent_file.md",
                domain="Test Domain"
            )
    
    def test_command_with_directory_path(self):
        """Test that command validation fails for directory paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError, match="Path is not a file"):
                ModelingCommand(
                    dda_path=temp_dir,
                    domain="Test Domain"
                )
    
    def test_output_path_creation(self):
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "new_dir", "output.json")
            command = ModelingCommand(
                dda_path="examples/sample_dda.md",
                domain="Test Domain",
                output_path=output_path
            )
            
            assert command.output_path == output_path
            assert os.path.exists(os.path.dirname(output_path))


class TestModelingCommandHandlerBasic:
    """Basic test cases for ModelingCommandHandler without Graphiti dependencies."""
    
    @pytest.fixture
    def mock_workflow(self):
        """Create a mock modeling workflow."""
        workflow = Mock(spec=ModelingWorkflow)
        workflow.execute = AsyncMock()
        return workflow
    
    @pytest.fixture
    def handler(self, mock_workflow):
        """Create a modeling command handler with mock workflow."""
        return ModelingCommandHandler(mock_workflow)
    
    @pytest.fixture
    def valid_command(self):
        """Create a valid modeling command."""
        return ModelingCommand(
            dda_path="examples/sample_dda.md",
            domain="Customer Analytics"
        )
    
    @pytest.mark.asyncio
    async def test_successful_handling(self, handler, mock_workflow, valid_command):
        """Test successful command handling."""
        # Setup mock result
        expected_result = ModelingResult(
            success=True,
            graph_document={"nodes": [], "relationships": []},
            artifacts={"summary": "test"}
        )
        mock_workflow.execute.return_value = expected_result
        
        # Execute handler
        result = await handler.handle(valid_command)
        
        # Verify results
        assert result.success is True
        assert result.graph_document == {"nodes": [], "relationships": []}
        assert result.artifacts == {"summary": "test"}
        mock_workflow.execute.assert_called_once_with(valid_command)
    
    @pytest.mark.asyncio
    async def test_failed_handling(self, handler, mock_workflow, valid_command):
        """Test command handling when workflow fails."""
        # Setup mock to raise exception
        mock_workflow.execute.side_effect = Exception("Test error")
        
        # Execute handler
        result = await handler.handle(valid_command)
        
        # Verify results
        assert result.success is False
        assert "Test error" in result.errors[0]
        mock_workflow.execute.assert_called_once_with(valid_command)


class TestModelingWorkflowBasic:
    """Basic test cases for ModelingWorkflow without Graphiti dependencies."""
    
    @pytest.fixture
    def mock_parser_factory(self):
        """Create a mock parser factory."""
        factory = Mock(spec=DDAParserFactory)
        return factory
    
    @pytest.fixture
    def mock_domain_modeler(self):
        """Create a mock domain modeler."""
        modeler = Mock()
        modeler.create_domain_graph = AsyncMock()
        modeler.update_domain_graph = AsyncMock()
        return modeler
    
    @pytest.fixture
    def workflow(self, mock_parser_factory, mock_domain_modeler):
        """Create a modeling workflow with mocks."""
        return ModelingWorkflow(mock_parser_factory, mock_domain_modeler)
    
    @pytest.fixture
    def sample_dda_document(self):
        """Create a sample DDA document for testing."""
        return DDADocument(
            domain="Test Domain",
            stakeholders=["Team A", "Team B"],
            data_owner="Test Owner",
            effective_date=datetime.now(),
            business_context="Test business context",
            entities=[
                DataEntity(
                    name="TestEntity",
                    description="Test entity description",
                    attributes=["attr1", "attr2"],
                    business_rules=["rule1"],
                    primary_key=None,
                    foreign_keys=[]
                )
            ],
            relationships=[
                Relationship(
                    source_entity="TestEntity",
                    target_entity="TestEntity",
                    relationship_type="1:N",
                    description="Test relationship"
                )
            ]
        )
    
    @pytest.mark.asyncio
    async def test_successful_workflow_execution(self, workflow, mock_parser_factory, mock_domain_modeler, sample_dda_document):
        """Test successful workflow execution."""
        # Setup mocks
        mock_parser = Mock()
        mock_parser.parse = AsyncMock(return_value=sample_dda_document)
        mock_parser_factory.get_parser.return_value = mock_parser
        
        mock_domain_modeler.create_domain_graph.return_value = {
            "nodes": [],
            "relationships": [],
            "domain": "Test Domain"
        }
        
        # Create command
        command = ModelingCommand(
            dda_path="examples/sample_dda.md",
            domain="Test Domain"
        )
        
        # Execute workflow
        result = await workflow.execute(command)
        
        # Verify results
        assert result["success"] is True
        assert result["graph_document"] is not None
        assert result["artifacts"] is not None
        assert len(result["warnings"]) == 0
        
        # Verify mocks were called
        mock_parser_factory.get_parser.assert_called_once_with("examples/sample_dda.md")
        mock_parser.parse.assert_called_once_with("examples/sample_dda.md")
        mock_domain_modeler.create_domain_graph.assert_called_once_with(sample_dda_document)
    
    @pytest.mark.asyncio
    async def test_workflow_with_validation_errors(self, workflow, mock_parser_factory, sample_dda_document):
        """Test workflow execution with validation errors."""
        # Create invalid DDA document (no domain)
        invalid_dda = sample_dda_document.model_copy()
        invalid_dda.domain = ""
        
        # Setup mocks
        mock_parser = Mock()
        mock_parser.parse = AsyncMock(return_value=invalid_dda)
        mock_parser_factory.get_parser.return_value = mock_parser
        
        # Create command
        command = ModelingCommand(
            dda_path="examples/sample_dda.md",
            domain="Test Domain"
        )
        
        # Execute workflow
        result = await workflow.execute(command)
        
        # Verify results
        assert result["success"] is False
        assert "Domain is required" in result["errors"]
    
    @pytest.mark.asyncio
    async def test_workflow_with_parser_exception(self, workflow, mock_parser_factory):
        """Test workflow execution when parser fails."""
        # Setup mock to raise exception
        mock_parser = Mock()
        mock_parser.parse = AsyncMock(side_effect=Exception("Parser error"))
        mock_parser_factory.get_parser.return_value = mock_parser
        
        # Create command
        command = ModelingCommand(
            dda_path="examples/sample_dda.md",
            domain="Test Domain"
        )
        
        # Execute workflow
        result = await workflow.execute(command)
        
        # Verify results
        assert result["success"] is False
        assert "Parser error" in result["errors"][0] 