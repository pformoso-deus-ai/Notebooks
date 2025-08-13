"""Stub client for the MCP (Model Composition Platform).

The MCP is a side service responsible for orchestrating model execution
and composition in the broader system.  The knowledge management
subsystem may call MCP to perform heavy document conversions or to
retrieve model outputs.  In this offline environment we provide a
minimal stub that simply records calls and returns an empty response.
"""

from typing import Any, Dict


class MCPClient:
    """Stub MCP client for demonstration and testing."""

    def __init__(self) -> None:
        # Record calls for verification in unit tests
        self.calls: list[tuple[str, Dict[str, Any]]] = []

    async def call_service(self, service_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call a side service.

        Args:
            service_name: The name of the service to call.
            payload: Arbitrary payload to send to the service.

        Returns:
            A dummy empty response.
        """
        self.calls.append((service_name, dict(payload)))
        # In a real implementation this would make an HTTP or RPC call
        return {}