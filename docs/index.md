# forgeevent

[![Release](https://img.shields.io/github/v/release/landygg/forgeevent-py)](https://img.shields.io/github/v/release/landygg/forgeevent-py)
[![Build status](https://img.shields.io/github/actions/workflow/status/landygg/forgeevent-py/main.yml?branch=main)](https://github.com/landygg/forgeevent-py/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/landygg/forgeevent-py)](https://img.shields.io/github/commit-activity/m/landygg/forgeevent-py)
[![License](https://img.shields.io/github/license/landygg/forgeevent-py)](https://img.shields.io/github/license/landygg/forgeevent-py)


`forgeevent` is a Python library for event management and dispatching, designed to be simple, flexible, and extensible.

## Key Features

- Register synchronous and asynchronous handlers
- Support for typed events (dataclasses, enums)
- Simple API for local event dispatch
- Easy integration with existing systems

## Main Modules

- `forgeevent.handlers.local`: Local event handler
- `forgeevent.typing`: Event types and aliases
- `forgeevent.handlers.base`: Base for custom handlers

## Installation

```bash
pip install forgeevent
```

## Quick Example

```python
from forgeevent.handlers.local import local_handler
from dataclasses import dataclass

@dataclass
class MyEvent:
    order_id: str

@local_handler.register(event_name="my_event")
def handle_my_event(event):
    event_name, payload = event
    print(f"Event received: {payload.order_id}")

import asyncio
asyncio.run(local_handler.handle(("my_event", MyEvent(order_id="123"))))
```

See the [Usage Guide](usage.md) and module reference for more details.
