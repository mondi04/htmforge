# htmforge

Type-safe, composable UI components for Python — server-side rendered, HTMX-first.

## Why htmforge?

- Type-safe props and validation via Pydantic v2.
- Small, composable Element primitives with automatic XSS protection.
- HTMX-first integration with typed enums and helpers.
- Framework adapters for FastAPI, Flask, and Django.

## Quick install

```bash
pip install htmforge
```

Verify:

```python
import htmforge
print(htmforge.__version__)
```

## Minimal example

```python
from htmforge import Component
from htmforge.elements import div, p

class Hello(Component):
    name: str
    def render(self):
        return div(p(f"Hello {self.name}"))

print(Hello(name='World').to_html())
```

## Features

- Elements
- Components
- HTMX integrations
- Framework adapters

Continue: Getting Started → Quickstart
