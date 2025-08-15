"""Abstract knowledge manager interface.

A knowledge manager acts as the orchestrator for applying knowledge events to
the graph.  Implementations may perform validation, reasoning, rule
application and escalation of complex operations.  The application layer
provides a concrete implementation suitable for simple needs.
"""

from abc import ABC, abstractmethod

from .event import KnowledgeEvent


class KnowledgeManager(ABC):
    """Abstract base class for knowledge managers."""

    @abstractmethod
    async def handle_event(self, event: KnowledgeEvent) -> None:
        """Process a knowledge event.

        Implementations should examine the event, perform any necessary
        validation or reasoning, and call the appropriate methods on a
        knowledge graph backend.  They may also delegate to other services
        for complex or escalated operations.
        """
        raise NotImplementedError
