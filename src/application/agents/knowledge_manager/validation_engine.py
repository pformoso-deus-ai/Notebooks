"""Advanced validation engine for knowledge graph operations."""

from typing import Dict, Any, List, Optional
from domain.kg_backends import KnowledgeGraphBackend
from domain.event import KnowledgeEvent
from domain.roles import Role


class ValidationEngine:
    """Advanced validation for knowledge graph operations."""

    def __init__(self, backend: KnowledgeGraphBackend):
        self.backend = backend
        self._validation_rules = self._initialize_validation_rules()

    def _initialize_validation_rules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize validation rules for different operations."""
        return {
            "create_entity": [
                {
                    "name": "required_id",
                    "validator": self._validate_required_id,
                    "severity": "error"
                },
                {
                    "name": "id_format",
                    "validator": self._validate_id_format,
                    "severity": "warning"
                },
                {
                    "name": "properties_structure",
                    "validator": self._validate_properties_structure,
                    "severity": "warning"
                },
                {
                    "name": "role_permission",
                    "validator": self._validate_role_permission,
                    "severity": "error"
                }
            ],
            "create_relationship": [
                {
                    "name": "required_fields",
                    "validator": self._validate_required_relationship_fields,
                    "severity": "error"
                },
                {
                    "name": "relationship_type",
                    "validator": self._validate_relationship_type,
                    "severity": "warning"
                },
                {
                    "name": "role_permission",
                    "validator": self._validate_role_permission,
                    "severity": "error"
                }
            ]
        }

    async def validate_event(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate a knowledge event using all applicable rules."""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "validation_details": []
        }
        
        # Get rules for this action
        rules = self._validation_rules.get(event.action, [])
        
        for rule in rules:
            try:
                rule_result = await rule["validator"](event)
                
                if rule_result["is_valid"]:
                    if rule_result.get("warnings"):
                        validation_result["warnings"].extend(rule_result["warnings"])
                else:
                    validation_result["is_valid"] = False
                    if rule_result.get("errors"):
                        validation_result["errors"].extend(rule_result["errors"])
                
                # Add validation details
                validation_result["validation_details"].append({
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "passed": rule_result["is_valid"],
                    "warnings": rule_result.get("warnings", []),
                    "errors": rule_result.get("errors", [])
                })
                
            except Exception as e:
                # Rule validation failed
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Validation rule '{rule['name']}' failed: {str(e)}")
                validation_result["validation_details"].append({
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "passed": False,
                    "errors": [f"Rule execution failed: {str(e)}"]
                })
        
        return validation_result

    async def _validate_required_id(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate that entity ID is provided."""
        entity_id = event.data.get("id")
        
        if not entity_id:
            return {
                "is_valid": False,
                "errors": ["Entity ID is required for create_entity operation"]
            }
        
        if not isinstance(entity_id, str):
            return {
                "is_valid": False,
                "errors": ["Entity ID must be a string"]
            }
        
        return {"is_valid": True}

    async def _validate_id_format(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate entity ID format."""
        entity_id = event.data.get("id", "")
        warnings = []
        
        # Check for common ID format issues
        if len(entity_id) > 100:
            warnings.append("Entity ID is very long (>100 characters)")
        
        if " " in entity_id:
            warnings.append("Entity ID contains spaces - consider using underscores or hyphens")
        
        if entity_id.lower() in ["null", "none", "undefined", ""]:
            warnings.append("Entity ID appears to be empty or invalid")
        
        # Check for special characters that might cause issues
        special_chars = ['<', '>', '"', "'", '&', '|', ';', '(', ')', '[', ']', '{', '}']
        if any(char in entity_id for char in special_chars):
            warnings.append("Entity ID contains special characters that might cause issues")
        
        return {
            "is_valid": True,
            "warnings": warnings
        }

    async def _validate_properties_structure(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate entity properties structure."""
        properties = event.data.get("properties", {})
        warnings = []
        
        if not isinstance(properties, dict):
            return {
                "is_valid": False,
                "errors": ["Properties must be a dictionary"]
            }
        
        # Check property keys
        for key, value in properties.items():
            if not isinstance(key, str):
                warnings.append(f"Property key '{key}' is not a string")
                continue
            
            if not key.strip():
                warnings.append("Empty property key found")
                continue
            
            # Check for reserved property names
            reserved_names = ["id", "_id", "type", "_type", "label", "_label"]
            if key.lower() in reserved_names:
                warnings.append(f"Property key '{key}' might conflict with system properties")
            
            # Check property values
            if value is None:
                warnings.append(f"Property '{key}' has null value")
            elif isinstance(value, (dict, list)) and len(str(value)) > 1000:
                warnings.append(f"Property '{key}' has very large value (>1000 characters)")
        
        return {
            "is_valid": True,
            "warnings": warnings
        }

    async def _validate_required_relationship_fields(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate required fields for relationship creation."""
        required_fields = ["source", "target", "type"]
        missing_fields = []
        
        for field in required_fields:
            if not event.data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "is_valid": False,
                "errors": [f"Missing required fields: {', '.join(missing_fields)}"]
            }
        
        return {"is_valid": True}

    async def _validate_relationship_type(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate relationship type."""
        rel_type = event.data.get("type", "")
        warnings = []
        
        if not isinstance(rel_type, str):
            return {
                "is_valid": False,
                "errors": ["Relationship type must be a string"]
            }
        
        # Check relationship type format
        if len(rel_type) > 50:
            warnings.append("Relationship type is very long (>50 characters)")
        
        if " " in rel_type:
            warnings.append("Relationship type contains spaces - consider using underscores or hyphens")
        
        # Check for common relationship type patterns
        if rel_type.lower() in ["relates", "related", "connection", "link"]:
            warnings.append("Relationship type is very generic - consider using more specific types")
        
        return {
            "is_valid": True,
            "warnings": warnings
        }

    async def _validate_role_permission(self, event: KnowledgeEvent) -> Dict[str, Any]:
        """Validate role permissions for the operation."""
        role = event.role
        action = event.action
        
        # Define role permissions
        role_permissions = {
            "create_entity": {
                Role.DATA_ARCHITECT: True,
                Role.DATA_ENGINEER: True,
                Role.KNOWLEDGE_MANAGER: True,
                Role.SYSTEM_ADMIN: True
            },
            "create_relationship": {
                Role.DATA_ARCHITECT: False,
                Role.DATA_ENGINEER: False,
                Role.KNOWLEDGE_MANAGER: True,
                Role.SYSTEM_ADMIN: True
            }
        }
        
        action_permissions = role_permissions.get(action, {})
        is_allowed = action_permissions.get(role, False)
        
        if not is_allowed:
            return {
                "is_valid": False,
                "errors": [f"Role '{role.value}' is not allowed to perform action '{action}'"]
            }
        
        return {"is_valid": True}

    async def validate_batch_operation(self, events: List[KnowledgeEvent]) -> Dict[str, Any]:
        """Validate a batch of knowledge events."""
        batch_result = {
            "is_valid": True,
            "total_events": len(events),
            "valid_events": 0,
            "invalid_events": 0,
            "event_results": []
        }
        
        for i, event in enumerate(events):
            event_result = await self.validate_event(event)
            batch_result["event_results"].append({
                "index": i,
                "event": event,
                "result": event_result
            })
            
            if event_result["is_valid"]:
                batch_result["valid_events"] += 1
            else:
                batch_result["invalid_events"] += 1
                batch_result["is_valid"] = False
        
        return batch_result

    def add_custom_rule(self, action: str, rule: Dict[str, Any]) -> None:
        """Add a custom validation rule."""
        if action not in self._validation_rules:
            self._validation_rules[action] = []
        
        self._validation_rules[action].append(rule)

    def remove_rule(self, action: str, rule_name: str) -> bool:
        """Remove a validation rule by name."""
        if action in self._validation_rules:
            for i, rule in enumerate(self._validation_rules[action]):
                if rule.get("name") == rule_name:
                    del self._validation_rules[action][i]
                    return True
        return False
