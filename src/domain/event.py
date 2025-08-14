"""Event definitions for knowledge management.

`KnowledgeEvent` describes an operation to be applied to the knowledge graph.
Each event carries an action string (e.g. ``create_entity`` or ``create_relationship``),
a ``data`` dictionary containing all necessary arguments for that action,
and the role of the caller.  The role is used by the knowledge manager
to enforce simple RBAC rules.
"""

from dataclasses import dataclass
from typing import Any, Dict

from .roles import Role


@dataclass
class KnowledgeEvent:
    """Event representing a knowledge graph operation.

    Attributes:
        action: A string identifying the type of operation.  Examples include
            ``"create_entity"`` and ``"create_relationship"``.  Unknown actions
            will result in a ``ValueError`` when processed by a knowledge
            manager.
        data: A dictionary containing the parameters needed to perform the
            action.  For ``create_entity`` this should contain an ``id`` key
            and optionally a ``properties`` mapping.  For ``create_relationship``
            this should include ``source``, ``target``, ``type`` and optionally
            ``properties``.
        role: The role of the caller, used to enforce access control.
    """

    action: str
    data: Dict[str, Any]
    role: Role

    def __post_init__(self) -> None:
        if not isinstance(self.role, Role):
            # Coerce from string if necessary to support JSON payloads
            try:
                object.__setattr__(self, "role", Role(self.role))  # type: ignore[misc]
            except ValueError as exc:
                raise ValueError(f"Invalid role: {self.role}") from exc
