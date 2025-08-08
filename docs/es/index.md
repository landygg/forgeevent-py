# forgeevent

> **Nota:** Esta documentación está disponible en inglés por defecto. Puedes cambiar a español usando el selector de idioma.

`forgeevent` es una librería Python para la gestión y dispatch de eventos, diseñada para ser simple, flexible y extensible.

## Características principales

- Registro de handlers síncronos y asíncronos
- Soporte para eventos tipados (dataclasses, enums)
- API simple para dispatch local de eventos
- Integración fácil con sistemas existentes

## Módulos principales

- `forgeevent.handlers.local`: Handler local para eventos
- `forgeevent.typing`: Tipos y alias para eventos
- `forgeevent.handlers.base`: Base para crear nuevos handlers

## Instalación

```bash
pip install forgeevent
```

## Ejemplo rápido

```python
from forgeevent.handlers.local import local_handler
from dataclasses import dataclass

@dataclass
class MyEvent:
    order_id: str

@local_handler.register(event_name="my_event")
def handle_my_event(event):
    event_name, payload = event
    print(f"Evento recibido: {payload.order_id}")

import asyncio
asyncio.run(local_handler.handle(("my_event", MyEvent(order_id="123"))))
```

Consulta la [Guía de Uso](usage.md) y la referencia de módulos para más detalles.
