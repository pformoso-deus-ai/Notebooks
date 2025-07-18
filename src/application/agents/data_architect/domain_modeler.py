from typing import Dict, Any, List
from domain.dda_models import DDADocument, DataEntity, Relationship

from graphiti_core import Graphiti


class DomainModeler:
    """Creates and updates domain knowledge graphs from DDA documents using a real Graphiti backend. Requires a real Graphiti instance for both graph and LLM operations."""
    
    def __init__(self, graph: Graphiti, llm: Graphiti):
        self.graph = graph
        self.llm = llm
    
    async def create_domain_graph(self, dda_document: DDADocument) -> Dict[str, Any]:
        """Create a new domain knowledge graph from DDA document."""
        
        nodes = []
        relationships = []
        
        # 1. Create domain node
        domain_node = await self.graph.upsert_node(
            "Domain",
            dda_document.domain,
            {
                "description": dda_document.business_context,
                "stakeholders": dda_document.stakeholders,
                "data_owner": dda_document.data_owner,
                "effective_date": dda_document.effective_date.isoformat()
            }
        )
        nodes.append(domain_node)
        
        # 2. Create entity nodes
        entity_nodes = []
        for entity in dda_document.entities:
            entity_node = await self.graph.upsert_node(
                "DataEntity",
                entity.name,
                {
                    "description": entity.description,
                    "attributes": entity.attributes,
                    "business_rules": entity.business_rules,
                    "primary_key": entity.primary_key,
                    "foreign_keys": entity.foreign_keys
                }
            )
            entity_nodes.append(entity_node)
            nodes.append(entity_node)
            
            # Create relationship to domain
            domain_relationship = await self.graph.upsert_relationship(
                "BELONGS_TO",
                entity_node.id,
                domain_node.id,
                {
                    "relationship_type": "entity_to_domain",
                    "description": f"Entity {entity.name} belongs to domain {dda_document.domain}"
                }
            )
            relationships.append(domain_relationship)
        
        # 3. Create entity relationships
        for relationship in dda_document.relationships:
            # Find source and target entity nodes
            source_node = next((node for node in entity_nodes if node.properties.get("name") == relationship.source_entity), None)
            target_node = next((node for node in entity_nodes if node.properties.get("name") == relationship.target_entity), None)
            
            if source_node and target_node:
                entity_relationship = await self.graph.upsert_relationship(
                    relationship.relationship_type,
                    source_node.id,
                    target_node.id,
                    {
                        "description": relationship.description,
                        "constraints": relationship.constraints,
                        "source_entity": relationship.source_entity,
                        "target_entity": relationship.target_entity
                    }
                )
                relationships.append(entity_relationship)
        
        return {
            "nodes": nodes,
            "relationships": relationships,
            "domain": dda_document.domain,
            "entities_count": len(entity_nodes),
            "relationships_count": len(relationships)
        }
    
    async def update_domain_graph(self, dda_document: DDADocument) -> Dict[str, Any]:
        """Update existing domain knowledge graph with new DDA information."""
        # For now, we'll just create a new graph
        # In a full implementation, you'd want to:
        # 1. Check if domain already exists
        # 2. Merge new entities with existing ones
        # 3. Update relationships
        # 4. Preserve existing data that's not in the new DDA
        
        return await self.create_domain_graph(dda_document)
    
    async def validate_graph(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the created knowledge graph."""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {
                "nodes_count": len(graph_data.get("nodes", [])),
                "relationships_count": len(graph_data.get("relationships", [])),
                "entities_count": len([n for n in graph_data.get("nodes", []) if n.get("type") == "DataEntity"]),
                "domains_count": len([n for n in graph_data.get("nodes", []) if n.get("type") == "Domain"])
            }
        }
        
        # Basic validation checks
        if validation_result["statistics"]["domains_count"] == 0:
            validation_result["errors"].append("No domain nodes found")
            validation_result["is_valid"] = False
        
        if validation_result["statistics"]["entities_count"] == 0:
            validation_result["errors"].append("No entity nodes found")
            validation_result["is_valid"] = False
        
        if validation_result["statistics"]["relationships_count"] == 0:
            validation_result["warnings"].append("No relationships found between entities")
        
        return validation_result 