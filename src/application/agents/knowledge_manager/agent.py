"""Knowledge Manager Agent for handling escalated and complex KG operations."""

from typing import Dict, Any, List, Optional
from domain.agent import Agent
from domain.communication import Message
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
import logging
import asyncio
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class KGUpdateType(Enum):
    """Types of KG updates that can be escalated to the knowledge manager."""
    COMPLEX_MERGE = "complex_merge"
    CONFLICT_RESOLUTION = "conflict_resolution"
    VALIDATION_FAILURE = "validation_failure"
    REASONING_REQUIRED = "reasoning_required"
    BATCH_UPDATE = "batch_update"
    ONTOLOGY_UPDATE = "ontology_update"


class KGUpdateRequest:
    """Request for knowledge graph update from other agents."""
    
    def __init__(
        self,
        update_type: KGUpdateType,
        source_agent: str,
        domain: str,
        entities: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        metadata: Dict[str, Any],
        priority: int = 1
    ):
        self.update_type = update_type
        self.source_agent = source_agent
        self.domain = domain
        self.entities = entities
        self.relationships = relationships
        self.metadata = metadata
        self.priority = priority
        self.timestamp = datetime.now(timezone.utc)
        self.request_id = f"{update_type.value}_{domain}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}"


class KGUpdateResult:
    """Result of knowledge graph update operation."""
    
    def __init__(
        self,
        success: bool,
        request_id: str,
        nodes_created: int = 0,
        edges_created: int = 0,
        conflicts_resolved: int = 0,
        validation_errors: List[str] = None,
        reasoning_applied: List[str] = None,
        rollback_performed: bool = False,
        error_message: str = None
    ):
        self.success = success
        self.request_id = request_id
        self.nodes_created = nodes_created
        self.edges_created = edges_created
        self.conflicts_resolved = conflicts_resolved
        self.validation_errors = validation_errors or []
        self.reasoning_applied = reasoning_applied or []
        self.rollback_performed = rollback_performed
        self.error_message = error_message
        self.timestamp = datetime.now(timezone.utc)


class KnowledgeManagerAgent(Agent):
    """Agent responsible for handling escalated and complex KG operations."""
    
    def __init__(self, graph: Graphiti, llm: Graphiti):
        # Note: We're not using the standard Agent constructor since this is a specialized agent
        # that doesn't need command_bus and communication_channel in the same way
        self.name = "knowledge_manager"
        self.description = "Handles complex KG operations and reasoning"
        self.graph = graph
        self.llm = llm
        self._update_queue = asyncio.Queue()
        self._processing = False
        self._audit_log = []
        
    async def start(self):
        """Start the knowledge manager agent."""
        logger.info("Starting Knowledge Manager Agent")
        self._processing = True
        asyncio.create_task(self._process_update_queue())
        
    async def stop(self):
        """Stop the knowledge manager agent."""
        logger.info("Stopping Knowledge Manager Agent")
        self._processing = False
    
    async def process_messages(self) -> None:
        """Process incoming messages (required by Agent abstract class)."""
        # This method is required by the Agent abstract class
        # but the knowledge manager processes messages differently
        # through the process_message method
        pass
        
    async def process_message(self, message: Message) -> Message:
        """Process incoming messages from other agents."""
        try:
            if message.content.get("type") == "kg_update_request":
                return await self._handle_kg_update_request(message)
            elif message.content.get("type") == "kg_query":
                return await self._handle_kg_query(message)
            elif message.content.get("type") == "validation_request":
                return await self._handle_validation_request(message)
            else:
                            return Message(
                sender_id=self.name,
                receiver_id=message.sender_id,
                content={"error": "Unknown message type"}
            )
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return Message(
                sender_id=self.name,
                receiver_id=message.sender_id,
                content={"error": str(e)}
            )
    
    async def escalate_update(self, update_request: KGUpdateRequest) -> KGUpdateResult:
        """Handle escalated KG update from other agents."""
        try:
            # Add to processing queue
            await self._update_queue.put(update_request)
            
            # Wait for processing (in a real implementation, this would be async)
            result = await self._process_update(update_request)
            
            # Log the operation
            self._audit_log.append({
                "timestamp": datetime.now(timezone.utc),
                "request_id": update_request.request_id,
                "source_agent": update_request.source_agent,
                "update_type": update_request.update_type.value,
                "success": result.success,
                "nodes_created": result.nodes_created,
                "edges_created": result.edges_created
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error in escalated update: {e}")
            return KGUpdateResult(
                success=False,
                request_id=update_request.request_id,
                error_message=str(e)
            )
    
    async def _process_update(self, update_request: KGUpdateRequest) -> KGUpdateResult:
        """Process a KG update request with validation and reasoning."""
        
        # Step 1: Validate the update
        validation_result = await self._validate_update(update_request)
        if not validation_result["valid"]:
            return KGUpdateResult(
                success=False,
                request_id=update_request.request_id,
                validation_errors=validation_result["errors"]
            )
        
        # Step 2: Check for conflicts
        conflicts = await self._detect_conflicts(update_request)
        if conflicts:
            resolved_conflicts = await self._resolve_conflicts(update_request, conflicts)
        else:
            resolved_conflicts = []
        
        # Step 3: Apply reasoning
        reasoning_results = await self._apply_reasoning(update_request)
        
        # Step 4: Perform the update
        try:
            update_result = await self._perform_update(update_request, resolved_conflicts)
            
            return KGUpdateResult(
                success=True,
                request_id=update_request.request_id,
                nodes_created=update_result.get("nodes_created", 0),
                edges_created=update_result.get("edges_created", 0),
                conflicts_resolved=len(resolved_conflicts),
                reasoning_applied=reasoning_results
            )
            
        except Exception as e:
            # Rollback on failure
            await self._perform_rollback(update_request)
            return KGUpdateResult(
                success=False,
                request_id=update_request.request_id,
                error_message=str(e),
                rollback_performed=True
            )
    
    async def _validate_update(self, update_request: KGUpdateRequest) -> Dict[str, Any]:
        """Validate the KG update request."""
        errors = []
        
        # Check for required fields
        if not update_request.domain:
            errors.append("Domain is required")
        
        if not update_request.entities and not update_request.relationships:
            errors.append("At least entities or relationships must be provided")
        
        # Validate entity structure
        for entity in update_request.entities:
            if not entity.get("name"):
                errors.append("Entity name is required")
        
        # Validate relationship structure
        for rel in update_request.relationships:
            if not rel.get("source") or not rel.get("target"):
                errors.append("Relationship source and target are required")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    async def _detect_conflicts(self, update_request: KGUpdateRequest) -> List[Dict[str, Any]]:
        """Detect conflicts with existing KG data."""
        conflicts = []
        
        # Check for entity name conflicts
        for entity in update_request.entities:
            existing_entities = await self._find_existing_entities(entity["name"])
            if existing_entities:
                conflicts.append({
                    "type": "entity_name_conflict",
                    "entity_name": entity["name"],
                    "existing_entities": existing_entities
                })
        
        # Check for relationship conflicts
        for rel in update_request.relationships:
            existing_rels = await self._find_existing_relationships(rel["source"], rel["target"])
            if existing_rels:
                conflicts.append({
                    "type": "relationship_conflict",
                    "source": rel["source"],
                    "target": rel["target"],
                    "existing_relationships": existing_rels
                })
        
        return conflicts
    
    async def _resolve_conflicts(self, update_request: KGUpdateRequest, conflicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve conflicts using reasoning and rules."""
        resolved_conflicts = []
        
        for conflict in conflicts:
            if conflict["type"] == "entity_name_conflict":
                # Apply entity merging logic
                resolution = await self._resolve_entity_conflict(conflict)
                resolved_conflicts.append(resolution)
            elif conflict["type"] == "relationship_conflict":
                # Apply relationship merging logic
                resolution = await self._resolve_relationship_conflict(conflict)
                resolved_conflicts.append(resolution)
        
        return resolved_conflicts
    
    async def _apply_reasoning(self, update_request: KGUpdateRequest) -> List[str]:
        """Apply symbolic reasoning to the update."""
        reasoning_results = []
        
        # Apply domain-specific rules
        domain_rules = await self._get_domain_rules(update_request.domain)
        for rule in domain_rules:
            result = await self._apply_rule(rule, update_request)
            if result:
                reasoning_results.append(f"Applied rule: {rule['name']} - {result}")
        
        # Apply consistency checks
        consistency_result = await self._check_consistency(update_request)
        if consistency_result:
            reasoning_results.append(f"Consistency check: {consistency_result}")
        
        return reasoning_results
    
    async def _perform_update(self, update_request: KGUpdateRequest, resolved_conflicts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform the actual KG update."""
        
        # Create episode content with resolved conflicts
        episode_content = self._create_episode_content(update_request, resolved_conflicts)
        
        # Add episode to Graphiti
        episode_results = await self.graph.add_episode(
            name=f"KG Update - {update_request.domain}",
            episode_body=episode_content,
            source_description=f"Escalated update from {update_request.source_agent}",
            reference_time=update_request.timestamp,
            source=EpisodeType.message,
            group_id=f"kg_update_{update_request.domain.lower().replace(' ', '_')}",
            update_communities=True
        )
        
        return {
            "nodes_created": len(episode_results.nodes) if episode_results.nodes else 0,
            "edges_created": len(episode_results.edges) if episode_results.edges else 0,
            "episode_uuid": episode_results.episode.uuid if episode_results.episode else None
        }
    
    async def _perform_rollback(self, update_request: KGUpdateRequest):
        """Perform rollback of failed update."""
        logger.warning(f"Performing rollback for request {update_request.request_id}")
        # In a real implementation, this would revert the KG to its previous state
        # For now, we just log the rollback
    
    async def _process_update_queue(self):
        """Process updates from the queue."""
        while self._processing:
            try:
                update_request = await asyncio.wait_for(self._update_queue.get(), timeout=1.0)
                await self._process_update(update_request)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing update queue: {e}")
    
    async def _handle_kg_update_request(self, message: Message) -> Message:
        """Handle KG update request from other agents."""
        try:
            # Parse the update request from message
            content = message.content
            update_request = KGUpdateRequest(
                update_type=KGUpdateType(content["update_type"]),
                source_agent=content["source_agent"],
                domain=content["domain"],
                entities=content.get("entities", []),
                relationships=content.get("relationships", []),
                metadata=content.get("metadata", {}),
                priority=content.get("priority", 1)
            )
            
            result = await self.escalate_update(update_request)
            
            return Message(
                sender_id=self.name,
                receiver_id=message.sender_id,
                content={
                    "type": "kg_update_response",
                    "request_id": result.request_id,
                    "success": result.success,
                    "nodes_created": result.nodes_created,
                    "edges_created": result.edges_created,
                    "conflicts_resolved": result.conflicts_resolved,
                    "validation_errors": result.validation_errors,
                    "reasoning_applied": result.reasoning_applied,
                    "error_message": result.error_message
                }
            )
        except Exception as e:
            return Message(
                sender_id=self.name,
                receiver_id=message.sender_id,
                content={
                    "type": "kg_update_response",
                    "success": False,
                    "error_message": str(e)
                }
            )
    
    async def _handle_kg_query(self, message: Message) -> Message:
        """Handle KG query requests."""
        # Implementation for KG queries
        return Message(
            sender_id=self.name,
            receiver_id=message.sender_id,
            content={"type": "kg_query_response", "data": []}
        )
    
    async def _handle_validation_request(self, message: Message) -> Message:
        """Handle validation requests."""
        # Implementation for validation requests
        return Message(
            sender_id=self.name,
            receiver_id=message.sender_id,
            content={"type": "validation_response", "valid": True}
        )
    
    # Helper methods (stubs for now)
    async def _find_existing_entities(self, name: str) -> List[Dict[str, Any]]:
        """Find existing entities with the given name."""
        # Implementation would query the KG
        return []
    
    async def _find_existing_relationships(self, source: str, target: str) -> List[Dict[str, Any]]:
        """Find existing relationships between source and target."""
        # Implementation would query the KG
        return []
    
    async def _resolve_entity_conflict(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve entity name conflict."""
        # Implementation would merge entities or create new ones
        return {"resolution": "merged", "conflict": conflict}
    
    async def _resolve_relationship_conflict(self, conflict: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve relationship conflict."""
        # Implementation would merge relationships or create new ones
        return {"resolution": "merged", "conflict": conflict}
    
    async def _get_domain_rules(self, domain: str) -> List[Dict[str, Any]]:
        """Get domain-specific rules for reasoning."""
        # Implementation would load domain rules
        return []
    
    async def _apply_rule(self, rule: Dict[str, Any], update_request: KGUpdateRequest) -> Optional[str]:
        """Apply a reasoning rule to the update."""
        # Implementation would apply the rule
        return None
    
    async def _check_consistency(self, update_request: KGUpdateRequest) -> Optional[str]:
        """Check consistency of the update."""
        # Implementation would check consistency
        return None
    
    def _create_episode_content(self, update_request: KGUpdateRequest, resolved_conflicts: List[Dict[str, Any]]) -> str:
        """Create episode content for the KG update."""
        content = f"""
# Knowledge Graph Update
**Domain:** {update_request.domain}
**Source Agent:** {update_request.source_agent}
**Update Type:** {update_request.update_type.value}
**Timestamp:** {update_request.timestamp}

## Entities
{chr(10).join([f"- {entity['name']}: {entity.get('description', 'No description')}" for entity in update_request.entities])}

## Relationships
{chr(10).join([f"- {rel['source']} -> {rel['target']}: {rel.get('type', 'unknown')}" for rel in update_request.relationships])}

## Resolved Conflicts
{chr(10).join([f"- {conflict['resolution']}: {conflict['conflict']}" for conflict in resolved_conflicts])}

## Metadata
{chr(10).join([f"- {key}: {value}" for key, value in update_request.metadata.items()])}
"""
        return content
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get the audit log of operations."""
        return self._audit_log.copy() 