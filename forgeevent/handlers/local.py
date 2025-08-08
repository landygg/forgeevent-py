"""
Local event handler for managing and dispatching events within the application.

This module provides the `LocalHandler` class, which allows registering event listeners, retrieving
registered listeners, and handling events asynchronously or synchronously.
"""

import asyncio
import logging
from collections.abc import Callable
from typing import Any, ClassVar

from forgeevent.handlers.base import BaseEventHandler
from forgeevent.typing import Event, EventName

logger = logging.getLogger(__name__)


class LocalHandler(BaseEventHandler):
    """
    Event handler that manages event listeners and dispatches events locally.

    This class allows registering listeners for specific event names and handles the execution
    of those listeners when an event is triggered. It supports both synchronous and asynchronous
    listeners.

    Attributes
    ----------
    _listeners : ClassVar[dict[EventName, list[Callable[..., Any]]]]
        Dictionary mapping event names to lists of listener functions.
    """

    _listeners: ClassVar[dict[EventName, list[Callable[..., Any]]]] = {}

    def _get_listeners(self, event_name: EventName) -> list[Callable[..., Any]]:
        """
        Retrieve the list of listeners for a specific event name.

        Parameters
        ----------
        event_name : EventName
            The name of the event to get listeners for.

        Returns
        -------
        list[Callable[..., Any]]
            The list of registered listeners for the event name.
        """
        return self._listeners.get(event_name, [])

    def _register_handler(self, event_name: EventName, listener: Callable[..., Any]) -> None:
        """
        Register a listener for a specific event name.

        Parameters
        ----------
        event_name : EventName
            The name of the event to register the listener for.
        listener : Callable[..., Any]
            The function to call when the event is triggered.
        """

        logger.debug(
            "Registering handler for event name: %s with listener: %s", event_name, listener
        )

        logger.debug("Current listeners for %s: %s", event_name, self._listeners)

        self._listeners.setdefault(event_name, []).append(listener)

        logger.debug("Updated listeners for %s: %s", event_name, self._listeners)

    def register(
        self, event_name: EventName, listener: Callable[..., Any] | None = None
    ) -> Callable[..., Any]:
        """
        Register a listener for a specific event name, optionally as a decorator.

        Parameters
        ----------
        event_name : EventName
            The name of the event to listen for.
        listener : Callable[..., Any] | None
            The function to register, or None if used as a decorator.

        Returns
        -------
        Callable[..., Any]
            The registered listener or a decorator.

        Examples
        --------
        As a decorator:
            @handler.register(event_name=MyEvent)
            def on_my_event(event):
                ...

        As a direct call:
            def on_my_event(event):
                ...
            handler.register(event_name=MyEvent, listener=on_my_event)
        """

        def wrapper(_listener: Callable[..., Any]) -> Callable[..., Any]:
            """
            Decorator to register a listener for an event name.
            Args:
                listener (Callable[..., Any]): The function to register as a listener.
            Returns:
                Callable[..., Any]: The wrapped listener function.
            """

            logger.debug("Wrapping listener for event name: %s", event_name)
            self._register_handler(event_name, _listener)
            return _listener

        if listener is None:
            logger.debug("Registering as a decorator when no listener is provided.")
            return wrapper

        logger.debug("Registering listener directly for event name: %s", event_name)
        return wrapper(_listener=listener)

    async def handle(self, event: Event[Any]) -> None:
        """
        Handle a single event.

        Parameters
        ----------
        event : Event
            The event to handle.
        """

        event_name, payload = event
        logger.debug("Handling event: %s with payload: %s", event_name, payload)

        listeners = self._get_listeners(event_name)

        if not listeners:
            logger.debug("No listeners registered for event name: %s", event_name)
            return

        for listener in listeners:
            if asyncio.iscoroutinefunction(listener):
                logger.debug(
                    "Calling async listener: %s for event: %s", listener.__name__, event_name
                )
                await listener(event)
            else:
                logger.debug("Calling sync listener: %s for event: %s", listener, event_name)
                # Run the synchronous listener in a separate thread to avoid blocking the event loop
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, listener, event)


local_handler = LocalHandler()
