from pydantic import BaseModel
from typing import Any, Dict


class ToolDefinition(BaseModel):
    """Represents the MCP-compliant definition of a tool."""

    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema for parameters 