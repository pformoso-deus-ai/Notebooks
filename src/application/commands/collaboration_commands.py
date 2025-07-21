from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from domain.commands import Command


@dataclass
class BuildKGCommand(Command):
    """Command to build knowledge graph from metadata."""
    metadata_uri: str


@dataclass
class KGFeedbackCommand(Command):
    """Command to provide feedback on knowledge graph quality."""
    kg_episode_uuid: str
    feedback_type: str  # "quality", "completeness", "accuracy", "suggestions"
    feedback_content: str
    rating: Optional[int] = None  # 1-5 scale
    suggestions: Optional[List[str]] = None


@dataclass
class NaturalLanguageQueryCommand(Command):
    """Command to query the knowledge graph using natural language."""
    query: str
    domain: Optional[str] = None
    max_results: int = 10


@dataclass
class ModelingFeedbackCommand(Command):
    """Command to provide feedback on domain modeling."""
    domain: str
    episode_uuid: str
    feedback_type: str  # "entity_quality", "relationship_accuracy", "domain_coverage", "suggestions"
    feedback_content: str
    rating: Optional[int] = None  # 1-5 scale
    entity_feedback: Optional[Dict[str, str]] = None  # Specific feedback on entities
    relationship_feedback: Optional[Dict[str, str]] = None  # Specific feedback on relationships
    suggestions: Optional[List[str]] = None


@dataclass
class CollaborativeRefinementCommand(Command):
    """Command to collaboratively refine domain models."""
    domain: str
    refinement_type: str  # "add_entities", "update_relationships", "merge_domains", "split_domains"
    refinement_data: Dict[str, Any]
    source_agent: str
    target_agent: str
    justification: str 