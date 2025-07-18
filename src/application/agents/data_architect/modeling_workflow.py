from typing import List, Optional
from pydantic import BaseModel
from domain.dda_models import DDADocument
from application.commands.modeling_command import ModelingCommand
from application.agents.data_architect.dda_parser import DDAParserFactory
from application.agents.data_architect.domain_modeler import DomainModeler


class ValidationResult(BaseModel):
    """Result of DDA document validation."""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []


class ModelingResult(BaseModel):
    """Result of the modeling workflow."""
    success: bool
    errors: List[str] = []
    warnings: List[str] = []
    graph_document: Optional[dict] = None
    artifacts: Optional[dict] = None


class ModelingWorkflow:
    """Orchestrates the complete modeling workflow."""
    
    def __init__(self, parser_factory: DDAParserFactory, domain_modeler: DomainModeler):
        self.parser_factory = parser_factory
        self.domain_modeler = domain_modeler
    
    async def execute(self, command: ModelingCommand) -> ModelingResult:
        """Execute the complete modeling workflow."""
        try:
            # 1. Parse DDA document
            parser = self.parser_factory.get_parser(command.dda_path)
            dda_document = await parser.parse(command.dda_path)
            
            # 2. Validate document
            validation_result = await self._validate_dda_document(dda_document)
            if not validation_result.is_valid:
                return ModelingResult(
                    success=False,
                    errors=validation_result.errors,
                    warnings=validation_result.warnings
                )
            
            # 3. Create or update knowledge graph
            if command.update_existing:
                graph_document = await self.domain_modeler.update_domain_graph(dda_document)
            else:
                graph_document = await self.domain_modeler.create_domain_graph(dda_document)
            
            # 4. Generate output artifacts
            artifacts = await self._generate_artifacts(dda_document, graph_document, command)
            
            return ModelingResult(
                success=True,
                graph_document=graph_document,
                artifacts=artifacts,
                warnings=validation_result.warnings
            )
            
        except Exception as e:
            return ModelingResult(
                success=False,
                errors=[f"Modeling workflow failed: {str(e)}"]
            )
    
    async def _validate_dda_document(self, dda_document: DDADocument) -> ValidationResult:
        """Validate the parsed DDA document."""
        errors = []
        warnings = []
        
        # Check required fields
        if not dda_document.domain:
            errors.append("Domain is required")
        
        if not dda_document.entities:
            errors.append("At least one data entity is required")
        
        # Check entity consistency
        entity_names = {entity.name for entity in dda_document.entities}
        for relationship in dda_document.relationships:
            if relationship.source_entity not in entity_names:
                errors.append(f"Relationship references unknown entity: {relationship.source_entity}")
            if relationship.target_entity not in entity_names:
                errors.append(f"Relationship references unknown entity: {relationship.target_entity}")
        
        # Check for common issues
        if len(dda_document.entities) > 0 and len(dda_document.relationships) == 0:
            warnings.append("No relationships defined between entities")
        
        if not dda_document.business_context or dda_document.business_context == "No business context provided":
            warnings.append("Business context is minimal or missing")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    async def _generate_artifacts(self, dda_document: DDADocument, graph_document: dict, command: ModelingCommand) -> dict:
        """Generate output artifacts from the modeling process."""
        artifacts = {
            "dda_summary": {
                "domain": dda_document.domain,
                "entities_count": len(dda_document.entities),
                "relationships_count": len(dda_document.relationships),
                "stakeholders": dda_document.stakeholders,
                "data_owner": dda_document.data_owner
            },
            "graph_summary": {
                "nodes_count": len(graph_document.get("nodes", [])),
                "relationships_count": len(graph_document.get("relationships", [])),
                "domain": dda_document.domain
            },
            "validation": {
                "is_valid": True,
                "timestamp": dda_document.effective_date.isoformat()
            }
        }
        
        return artifacts 