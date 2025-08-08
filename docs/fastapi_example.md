# FastAPI Integration Example

This section demonstrates how to integrate `forgeevent` with a FastAPI-like application, showing how to register event listeners and dispatch events in an async context.

## Event and Listener Definitions

First, define your event dataclasses and event types:

```python
from dataclasses import dataclass
from enum import Enum
from forgeevent.handlers.local import LocalHandler
from forgeevent.typing import Event

@dataclass
class AbsPaymentEvent:
    order_id: str

@dataclass
class PaymentSucceededEvent(AbsPaymentEvent):
    pass

@dataclass
class PaymentFailedEvent(AbsPaymentEvent):
    error: str

class EventType(Enum):
    PAYMENT_FAILED = "PaymentFailedEvent"
    PAYMENT_SUCCEEDED = "PaymentSucceededEvent"

async def handle_payment_failed_model(event: Event[PaymentFailedEvent]) -> None:
    """
    Handle payment failed events.
    """
    event_name, payload = event
    print(
        f"Handling event {event_name} for order_id: {payload.order_id} with error: {payload.error}"
    )

def register_listeners(local_handler: LocalHandler) -> None:
    local_handler.register(
        event_name=EventType.PAYMENT_FAILED, listener=handle_payment_failed_model
    )
```

## Application Lifespan and Event Dispatch

You can use an async context manager to manage application startup and shutdown, similar to FastAPI's lifespan events:


```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from forgeevent.handlers.local import local_handler
from test_registry import EventType, register_listeners, PaymentFailedEvent

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_listeners(local_handler)
    print("ProviderFactory and PaymentService initialized.")
    yield
    print("Cleaning up resources...")

app = FastAPI(lifespan=lifespan)

@app.post("/pay/fail")
async def trigger_failed_payment(order_id: str, error: str):
    """
    Endpoint to simulate a failed payment event and dispatch it through forgeevent.
    """
    await local_handler.handle((
        EventType.PAYMENT_FAILED,
        PaymentFailedEvent(order_id=order_id, error=error),
    ))
    return {"status": "event dispatched"}

# To run the FastAPI app:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_fastapi:app", host="127.0.0.1", port=8000, reload=True)
```

## How it works
- The `register_listeners` function registers your event handlers with the local handler.
- The `lifespan` context manager simulates FastAPI's startup/shutdown hooks.
- The `main` function dispatches a sample event, which will trigger the registered handler.

This pattern can be adapted to real FastAPI applications using the `lifespan` event or dependency injection.

---
For more advanced usage, see the [Usage Guide](usage.md) and the API Reference.
