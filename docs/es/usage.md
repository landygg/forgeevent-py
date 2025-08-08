# Guía de Uso

Esta guía explica cómo usar la librería `forgeevent` para gestionar y despachar eventos en tus aplicaciones Python.

## Instalación

Instala la librería y sus dependencias (requiere Python 3.9+):

```bash
pip install forgeevent
```

O, si desarrollas localmente:

```bash
make install
```

## Conceptos Básicos

- **Evento**: Una tupla de (event_name, payload), donde `event_name` es un string o Enum, y `payload` es cualquier objeto (usualmente un dataclass).
- **Handler**: Una función (sync o async) registrada para responder a un tipo de evento específico.
- **LocalHandler**: La clase principal para registrar y despachar eventos localmente.

## Definiendo Eventos

Puedes definir tus payloads de evento usando dataclasses:

```python
from dataclasses import dataclass

@dataclass
class PaymentSucceededEvent:
    order_id: str
    amount: float
    currency: str = "USD"
```

## Registrando Handlers

Puedes registrar handlers usando el decorador `@local_handler.register`:

```python
from forgeevent.handlers.local import local_handler

@local_handler.register(event_name="payment_successful")
def handle_payment(event):
    event_name, payload = event
    print(f"Pago exitoso: {payload}")
```

También puedes registrar handlers asíncronos:

```python
@local_handler.register(event_name="payment_successful")
async def notify_payment(event):
    event_name, payload = event
    # enviar notificación
```

## Despachando Eventos

Para despachar (lanzar) un evento:

```python
import asyncio

async def main():
    await local_handler.handle(("payment_successful", PaymentSucceededEvent(order_id="123", amount=100.0)))

asyncio.run(main())
```

## Avanzado: Usando Enums para Nombres de Evento

```python
from enum import Enum

class EventType(Enum):
    PAYMENT_SUCCESSFUL = "payment_successful"

@local_handler.register(event_name=EventType.PAYMENT_SUCCESSFUL)
def handle_payment(event):
    ...
```

## Testeo de Handlers

Puedes testear tus handlers usando pytest y pytest-asyncio. Consulta la carpeta `tests/` para ejemplos.

---

Para más detalles, revisa la Referencia de la API y el [código fuente](https://github.com/landygg/forgeevent-py).
