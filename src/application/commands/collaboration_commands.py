from pydantic import BaseModel
from typing import List, Dict, Any

from src.domain.commands import Command

class BuildKGCommand(Command, BaseModel):
    """
    A command to instruct the DataEngineerAgent to build a knowledge graph.
    """
    metadata_uri: str  # e.g., a path to a file or a database table

class KGFeedbackCommand(Command, BaseModel):
    """
    A command to provide feedback from the DataEngineerAgent to the DataArchitectAgent.
    """
    issues: List[Dict[str, Any]]  # e.g., [{"type": "dangling_relationship", "node_id": "x"}]

class NaturalLanguageQueryCommand(Command, BaseModel):
    """
    A command for the DataArchitectAgent to ask a natural language question.
    """
    query: str 