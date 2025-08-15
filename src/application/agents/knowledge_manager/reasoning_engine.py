"""Reasoning engine for applying symbolic logic to knowledge graph operations."""

from typing import Dict, Any, List, Optional
from domain.kg_backends import KnowledgeGraphBackend
from domain.event import KnowledgeEvent


class ReasoningEngine:
    """Applies symbolic reasoning and logic to knowledge graph operations."""

    def __init__(self, backend: KnowledgeGraphBackend):
        self.backend = backend
        self._reasoning_rules = self._initialize_reasoning_rules()

    def _initialize_reasoning_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize reasoning rules for different operations."""
        return {
            "create_entity": [
                {
                    "name": "property_inference",
                    "reasoner": self._infer_properties,
                    "priority": "high"
                },
                {
                    "name": "entity_classification",
                    "reasoner": self._classify_entity,
                    "priority": "medium"
                },
                {
                    "name": "relationship_suggestion",
                    "reasoner": self._suggest_relationships,
                    "priority": "low"
                }
            ],
            "create_relationship": [
                {
                    "name": "relationship_validation",
                    "reasoner": self._validate_relationship_logic,
                    "priority": "high"
                },
                {
                    "name": "inverse_relationship",
                    "reasoner": self._suggest_inverse_relationship,
                    "priority": "medium"
                },
                {
                    "name": "transitive_closure",
                    "reasoner": self._apply_transitive_closure,
                    "priority": "low"
                }
            ]
        }

    async def apply_reasoning(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Apply reasoning to a knowledge event."""
        reasoning_result = {
            "applied_rules": [],
            "inferences": [],
            "suggestions": [],
            "warnings": [],
            "reasoning_time": "0ms"
        }
        
        import time
        start_time = time.time()
        
        # Get rules for this action
        rules = self._reasoning_rules.get(event.action, [])
        
        # Sort rules by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_rules = sorted(rules, key=lambda r: priority_order.get(r["priority"], 3))
        
        for rule in sorted_rules:
            try:
                rule_result = await rule["reasoner"](event)
                
                if rule_result:
                    reasoning_result["applied_rules"].append(rule["name"])
                    
                    if rule_result.get("inferences"):
                        reasoning_result["inferences"].extend(rule_result["inferences"])
                    
                    if rule_result.get("suggestions"):
                        reasoning_result["suggestions"].extend(rule_result["suggestions"])
                    
                    if rule_result.get("warnings"):
                        reasoning_result["warnings"].extend(rule_result["warnings"])
                
            except Exception as e:
                reasoning_result["warnings"].append(f"Reasoning rule '{rule['name']}' failed: {str(e)}")
        
        # Calculate reasoning time
        reasoning_time = (time.time() - start_time) * 1000
        reasoning_result["reasoning_time"] = f"{reasoning_time:.2f}ms"
        
        return reasoning_result

    async def _infer_properties(self, event: KnowledgeEvent) -> Optional[Dict[str, Any]]:
        """Infer additional properties for an entity based on existing data."""
        entity_id = event.data.get("id", "")
        properties = event.data.get("properties", {})
        inferences = []
        
        # Infer entity type based on ID patterns
        if entity_id:
            if entity_id.lower().endswith(("_id", "id")):
                inferences.append({
                    "property": "entity_type",
                    "value": "identifier",
                    "confidence": 0.8,
                    "reason": "ID pattern suggests identifier entity"
                })
            
            if any(keyword in entity_id.lower() for keyword in ["user", "customer", "person"]):
                inferences.append({
                    "property": "entity_type",
                    "value": "person",
                    "confidence": 0.7,
                    "reason": "ID contains person-related keywords"
                })
            
            if any(keyword in entity_id.lower() for keyword in ["order", "transaction", "purchase"]):
                inferences.append({
                    "property": "entity_type",
                    "value": "transaction",
                    "confidence": 0.7,
                    "reason": "ID contains transaction-related keywords"
                })
        
        # Infer properties based on existing properties
        if "email" in properties:
            inferences.append({
                "property": "has_contact_info",
                "value": True,
                "confidence": 0.9,
                "reason": "Entity has email property"
            })
        
        if "created_date" in properties:
            inferences.append({
                "property": "is_temporal",
                "value": True,
                "confidence": 0.8,
                "reason": "Entity has temporal properties"
            })
        
        return {"inferences": inferences} if inferences else None

    async def _classify_entity(self, event: KnowledgeEvent) -> Optional[Dict[str, Any]]:
        """Classify entity based on properties and patterns."""
        properties = event.data.get("properties", {})
        suggestions = []
        
        # Classify based on property patterns
        if "name" in properties and "email" in properties:
            suggestions.append({
                "classification": "person",
                "confidence": 0.8,
                "reason": "Has name and email properties"
            })
        
        if "amount" in properties or "price" in properties:
            suggestions.append({
                "classification": "financial",
                "confidence": 0.7,
                "reason": "Has financial properties"
            })
        
        if "status" in properties and "created_date" in properties:
            suggestions.append({
                "classification": "process",
                "confidence": 0.6,
                "reason": "Has status and temporal properties"
            })
        
        return {"suggestions": suggestions} if suggestions else None

    async def _suggest_relationships(self, event: KnowledgeEvent) -> Optional[Dict[str, Any]]:
        """Suggest potential relationships for the entity."""
        entity_id = event.data.get("id", "")
        properties = event.data.get("properties", {})
        suggestions = []
        
        # Suggest relationships based on entity type
        if "email" in properties:
            suggestions.append({
                "relationship_type": "HAS_EMAIL",
                "target_pattern": "email_*",
                "confidence": 0.7,
                "reason": "Entity has email property"
            })
        
        if "created_date" in properties:
            suggestions.append({
                "relationship_type": "CREATED_ON",
                "target_pattern": "date_*",
                "confidence": 0.6,
                "reason": "Entity has creation date"
            })
        
        return {"suggestions": suggestions} if suggestions else None

    async def _validate_relationship_logic(self, event: KnowledgeEvent) -> Optional[Dict[str, Any]]:
        """Validate the logical consistency of a relationship."""
        source = event.data.get("source", "")
        target = event.data.get("target", "")
        rel_type = event.data.get("type", "")
        warnings = []
        
        # Check for logical inconsistencies
        if source == target and rel_type.lower() in ["is_a", "instance_of", "subclass_of"]:
            warnings.append({
                "type": "logical_inconsistency",
                "message": "Entity cannot be a subclass or instance of itself",
                "severity": "high"
            })
        
        # Check for relationship type patterns
        if rel_type.lower() in ["is_a", "instance_of"] and not rel_type[0].isupper():
            warnings.append({
                "type": "naming_convention",
                "message": "Taxonomic relationships should use PascalCase",
                "severity": "low"
            })
        
        return {"warnings": warnings} if warnings else None

    async def _suggest_inverse_relationship(self, event: KnowledgeEvent) -> Optional[Dict[str, Any]]:
        """Suggest inverse relationships."""
        rel_type = event.data.get("type", "")
        suggestions = []
        
        # Common inverse relationship patterns
        inverse_patterns = {
            "is_a": "has_instance",
            "has_part": "part_of",
            "owns": "owned_by",
            "manages": "managed_by",
            "reports_to": "has_subordinate"
        }
        
        if rel_type in inverse_patterns:
            suggestions.append({
                "inverse_type": inverse_patterns[rel_type],
                "confidence": 0.8,
                "reason": f"Standard inverse of '{rel_type}' relationship"
            })
        
        return {"suggestions": suggestions} if suggestions else None

    async def _apply_transitive_closure(self, event: KnowledgeEvent) -> Optional[Dict[str, Any]]:
        """Apply transitive closure for hierarchical relationships."""
        rel_type = event.data.get("type", "")
        suggestions = []
        
        # Transitive relationships
        transitive_types = ["is_a", "subclass_of", "part_of", "contains"]
        
        if rel_type in transitive_types:
            suggestions.append({
                "transitive_closure": True,
                "confidence": 0.9,
                "reason": f"'{rel_type}' is a transitive relationship"
            })
        
        return {"suggestions": suggestions} if suggestions else None

    async def apply_advanced_reasoning(self, events: List[KnowledgeEvent]) -> Dict[str, Any]:
        """Apply advanced reasoning across multiple events."""
        advanced_result = {
            "cross_event_inferences": [],
            "consistency_checks": [],
            "optimization_suggestions": []
        }
        
        # Cross-event consistency checks
        entity_ids = set()
        relationship_types = set()
        
        for event in events:
            if event.action == "create_entity":
                entity_id = event.data.get("id")
                if entity_id:
                    entity_ids.add(entity_id)
            
            elif event.action == "create_relationship":
                rel_type = event.data.get("type")
                if rel_type:
                    relationship_types.add(rel_type)
        
        # Check for orphaned relationships
        for event in events:
            if event.action == "create_relationship":
                source = event.data.get("source")
                target = event.data.get("target")
                
                if source and source not in entity_ids:
                    advanced_result["consistency_checks"].append({
                        "type": "orphaned_relationship",
                        "message": f"Relationship source '{source}' has no corresponding entity",
                        "severity": "high"
                    })
                
                if target and target not in entity_ids:
                    advanced_result["consistency_checks"].append({
                        "type": "orphaned_relationship",
                        "message": f"Relationship target '{target}' has no corresponding entity",
                        "severity": "high"
                    })
        
        # Suggest relationship optimizations
        if len(relationship_types) > 10:
            advanced_result["optimization_suggestions"].append({
                "type": "relationship_consolidation",
                "message": "Consider consolidating similar relationship types",
                "severity": "medium"
            })
        
        return advanced_result

    def add_custom_reasoning_rule(self, action: str, rule: Dict[str, Any]) -> None:
        """Add a custom reasoning rule."""
        if action not in self._reasoning_rules:
            self._reasoning_rules[action] = []
        
        self._reasoning_rules[action].append(rule)

    def remove_reasoning_rule(self, action: str, rule_name: str) -> bool:
        """Remove a reasoning rule by name."""
        if action in self._reasoning_rules:
            for i, rule in enumerate(self._reasoning_rules[action]):
                if rule.get("name") == rule_name:
                    del self._reasoning_rules[action][i]
                    return True
        return False
