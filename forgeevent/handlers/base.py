"""
Base classes for event handlers in the forgeevent framework.

This module provides the abstract base class `BaseEventHandler`,
which defines the interface for handling events.
Subclasses must implement the `handle` method to define how individual events are processed.
"""

import abc
import asyncio
from abc import ABC
from collections.abc import Iterable
from typing import Any

from forgeevent.typing import Event


class BaseEventHandler(ABC):
    """
    Abstract base class for event handlers.

    This class defines the interface for handling events.
    Subclasses must implement the `handle` method
    to define how individual events are processed.

    Methods
    -------
    dispatch(events: Iterable[Event]) -> None
        Asynchronously dispatches a collection of events by handling each event.
    handle(event: Event) -> None
        Abstract method to handle a single event. Must be implemented by subclasses.
    """

    async def dispatch(self, events: Iterable[Event[Any]]) -> None:
        """
        Dispatch a collection of events by asynchronously handling each event.

        Parameters
        ----------
        events : Iterable[Event]
            An iterable of Event objects to be handled.
        """
        await asyncio.gather(*[self.handle(event) for event in events])

    @abc.abstractmethod
    async def handle(self, event: Event[Any]) -> None:
        """
        Handle a single event.

        Parameters
        ----------
        event : Event
            The event to handle.
        """
        raise NotImplementedError
