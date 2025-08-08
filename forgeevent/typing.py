"""
Type definitions and aliases for ForgeEvent.

This module provides type hints and utility types for event handling,
payloads, and ASGI application interfaces, leveraging Pydantic models
and standard Python typing constructs.
"""

from enum import Enum
from typing import Any, TypeVar

EventName = str | Enum
EventPayload = TypeVar("EventPayload", bound=Any)
Event = tuple[EventName, EventPayload]
