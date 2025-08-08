# Usage Guide

This guide explains how to use the `forgeevent` library to manage and dispatch events in your Python applications.

## Installation

Install the library and its dependencies (requires Python 3.9+):

```bash
pip install forgeevent
```

Or, if you are developing locally:

```bash
make install
```

## Basic Concepts

- **Event**: A tuple of (event_name, payload), where `event_name` is a string or Enum, and `payload` is any object (often a dataclass).
- **Handler**: A function (sync or async) registered to respond to a specific event type.
- **LocalHandler**: The main class for registering and dispatching events locally.

## Defining Events

You can define your event payloads using dataclasses:

```python
from dataclasses import dataclass

@dataclass
class PaymentSucceededEvent:
    order_id: str
    amount: float
    currency: str = "USD"
```

## Registering Handlers

You can register handlers using the `@local_handler.register` decorator:

```python
from forgeevent.handlers.local import local_handler

@local_handler.register(event_name="payment_successful")
def handle_payment(event):
    event_name, payload = event
    print(f"Payment succeeded: {payload}")
```

You can also register async handlers:

```python
@local_handler.register(event_name="payment_successful")
async def notify_payment(event):
    event_name, payload = event
    # send notification
```

## Dispatching Events

To dispatch (trigger) an event:

```python
import asyncio

async def main():
    await local_handler.handle(("payment_successful", PaymentSucceededEvent(order_id="123", amount=100.0)))

asyncio.run(main())
```

## Advanced: Using Enums for Event Names

```python
from enum import Enum

class EventType(Enum):
    PAYMENT_SUCCESSFUL = "payment_successful"

@local_handler.register(event_name=EventType.PAYMENT_SUCCESSFUL)
def handle_payment(event):
    ...
```

## Testing Handlers

You can test your handlers using pytest and pytest-asyncio. See the `tests/` folder for examples.

---

For more details, see the API Reference and the [source code](https://github.com/landygg/forgeevent-py).
