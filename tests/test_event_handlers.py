import logging
from dataclasses import dataclass
from enum import Enum

import pytest

from forgeevent.handlers.local import local_handler
from forgeevent.typing import Event

logger = logging.getLogger(__name__)


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
    logger.debug(f"[Notifying]:: {event_name} with payload: {payload}")


@local_handler.register(event_name=EventType.PAYMENT_SUCCESSFUL)
async def log_payment_successful(event: Event[PaymentSucceededEvent]) -> None:
    """
    Log payment successful events.
    """
    event_name, payload = event
    logger.debug(f"[Log]:: {event_name} with payload: {payload}")


async def handle_payment_failed(event: Event[PaymentFailedEvent]) -> None:
    """
    Handle payment failed events.
    """
    _, payload = event

    logger.debug(
        f"Handling failed payment for order_id: {payload.order_id} with error: {payload.error}"
    )


local_handler.register(event_name=EventType.PAYMENT_FAILED, listener=handle_payment_failed)


@local_handler.register(event_name=EventType.PAYMENT_PENDING)
def handle_payment_pending(event: Event[PaymentPendingEvent]) -> None:
    """
    Handle payment pending events.
    """
    _, payload = event
    logger.debug(
        f"Handling pending payment for order_id: {payload.order_id} with transaction_id: {payload.transaction_id}"
    )


@pytest.mark.asyncio
async def test_handle_payment_successful(caplog):
    caplog.set_level(logging.DEBUG)
    event = (
        EventType.PAYMENT_SUCCESSFUL,
        PaymentSucceededEvent(order_id="order_1", amount=50.0, currency="USD"),
    )
    await local_handler.handle(event)
    assert any("[Notifying]::" in m for m in caplog.messages)
    assert any("[Log]::" in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_handle_payment_failed(caplog):
    caplog.set_level(logging.DEBUG)
    event = (
        EventType.PAYMENT_FAILED,
        PaymentFailedEvent(order_id="order_2", error="Card declined"),
    )
    await local_handler.handle(event)
    assert any("Handling failed payment for order_id: order_2" in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_handle_payment_pending(caplog):
    caplog.set_level(logging.DEBUG)
    event = (
        EventType.PAYMENT_PENDING,
        PaymentPendingEvent(order_id="order_3", transaction_id="tx_123"),
    )
    await local_handler.handle(event)
    assert any("Handling pending payment for order_id: order_3" in m for m in caplog.messages)
