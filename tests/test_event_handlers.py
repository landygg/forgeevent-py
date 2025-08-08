"# tests/test_event_handlers.py"

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

import pytest
from _pytest.logging import LogCaptureFixture

from forgeevent.handlers.base import BaseEventHandler
from forgeevent.handlers.local import local_handler
from forgeevent.typing import Event

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class AbsPaymentEvent:
    order_id: str


@dataclass
class PaymentFailedEvent(AbsPaymentEvent):
    __event_name__ = "PaymentFailedEvent"
    error: str


@dataclass
class PaymentSucceededEvent(AbsPaymentEvent):
    __event_name__ = "PaymentSucceededEvent"

    message: str = "Payment succeeded"
    amount: float = 0.0
    currency: str = "USD"


@dataclass
class PaymentPendingEvent(AbsPaymentEvent):
    __event_name__ = "PaymentPendingEvent"
    transaction_id: str = "pending_transaction"


class EventType(Enum):
    PAYMENT_SUCCESSFUL = "PaymentSuccessfulEvent"
    PAYMENT_FAILED = "PaymentFailedEvent"
    PAYMENT_PENDING = "PaymentPendingEvent"


@local_handler.register(event_name=EventType.PAYMENT_SUCCESSFUL)
async def notification_payment_successful(event: Event[PaymentSucceededEvent]) -> None:
    """
    Notify payment successful events.
    """
    event_name, payload = event
    logger.debug("[Notifying]:: %s with payload: %s", event_name, payload)


@local_handler.register(event_name=EventType.PAYMENT_SUCCESSFUL)
async def log_payment_successful(event: Event[PaymentSucceededEvent]) -> None:
    """
    Log payment successful events.
    """
    event_name, payload = event
    logger.debug("[Log]:: %s with payload: %s", event_name, payload)


async def handle_payment_failed(event: Event[PaymentFailedEvent]) -> None:
    """
    Handle payment failed events.
    """
    _, payload = event

    logger.debug(
        "Handling failed payment for order_id: %s with error: %s",
        payload.order_id,
        payload.error,
    )


local_handler.register(event_name=EventType.PAYMENT_FAILED, listener=handle_payment_failed)


@local_handler.register(event_name=EventType.PAYMENT_PENDING)
def handle_payment_pending(event: Event[PaymentPendingEvent]) -> None:
    """
    Handle payment pending events.
    """
    _, payload = event

    logger.debug(
        "Handling pending payment for order_id: %s with transaction_id: %s",
        payload.order_id,
        payload.transaction_id,
    )


def evaluate_logging(message: str, caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    assert any(message in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_handle_payment_successful(caplog: LogCaptureFixture):
    event = (
        EventType.PAYMENT_SUCCESSFUL,
        PaymentSucceededEvent(order_id="order_1", amount=50.0, currency="USD"),
    )
    await local_handler.handle(event)
    evaluate_logging("[Notifying]::", caplog)
    evaluate_logging("[Log]::", caplog)


@pytest.mark.asyncio
async def test_handle_payment_failed(caplog: LogCaptureFixture):
    caplog.set_level(logging.DEBUG)
    event = (
        EventType.PAYMENT_FAILED,
        PaymentFailedEvent(order_id="order_2", error="Card declined"),
    )
    await local_handler.handle(event)
    evaluate_logging(
        "Handling failed payment for order_id: order_2 with error: Card declined", caplog
    )


@pytest.mark.asyncio
async def test_handle_payment_pending(caplog: LogCaptureFixture):
    event = (
        EventType.PAYMENT_PENDING,
        PaymentPendingEvent(order_id="order_3", transaction_id="tx_123"),
    )
    await local_handler.handle(event)
    evaluate_logging(
        "Handling pending payment for order_id: order_3 with transaction_id: tx_123", caplog
    )


@pytest.mark.asyncio
async def test_dispatch_payment_events(caplog: LogCaptureFixture):
    events = [
        (
            EventType.PAYMENT_SUCCESSFUL,
            PaymentSucceededEvent(order_id="order_1", amount=50.0, currency="USD"),
        ),
    ]
    await local_handler.dispatch(events)
    evaluate_logging("[Notifying]::", caplog)
    evaluate_logging("[Log]::", caplog)


class TestBaseEventHandler(BaseEventHandler):
    """Test class for BaseEventHandler to ensure NotImplementedError is raised."""

    async def handle(self, event: Any) -> None:
        await super().handle(event)


@pytest.mark.asyncio
async def test_base_handle_not_implemented():
    handler = TestBaseEventHandler()
    with pytest.raises(NotImplementedError):
        await handler.handle((
            EventType.PAYMENT_SUCCESSFUL,
            PaymentSucceededEvent(order_id="order_1"),
        ))
