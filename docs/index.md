# htmforge

Type-safe, composable UI components for Python that render server-side and play well with HTMX.

## Why htmforge?

- `cls="container"` → `class="container"` automatically, so you can keep Pythonic names without losing HTML output.
- `for_="email"` → `for="email"`, while `disabled=True` renders as a flag and `hidden=False` disappears entirely.
- `hx_get="/search"` and `hx_trigger=HxTrigger.KEYUP` stay typed, so HTMX attributes are assembled without string juggling.
- `Component(...).to_html()` gives you safe HTML, and the same component can be adapted with `to_fastapi()`, `to_flask()`, or `to_django()`.

## Quick install

```bash
pip install htmforge
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

## Component overview

| Component   | Description                                      | Import |
|-------------|--------------------------------------------------|--------|
| Alert       | Dismissible info/success/warning/error box       | `from htmforge.components import Alert` |
| Badge       | Small inline label with variant classes          | `from htmforge.components import Badge` |
| Breadcrumb  | Ordered nav with `aria-current` for current item | `from htmforge.components import Breadcrumb` |
| DataTable   | Table with optional HTMX reloading               | `from htmforge.components import DataTable` |
| FormField   | Label + input + optional error block             | `from htmforge.components import FormField` |
| Modal       | Trigger button + `<dialog>` overlay (HTMX body)  | `from htmforge.components import Modal` |
| Page        | Abstract full-page component (adds DOCTYPE)      | `from htmforge.components.page import Page` |
| Pagination  | Page links + prev/next, supports HTMX targets    | `from htmforge.components import Pagination` |
| SearchInput | Search input with `keyup` debounce via HTMX      | `from htmforge.components import SearchInput` |

## What you get

```python
from htmforge import Component
from htmforge.elements import div, p

class Card(Component):
    title: str
    body: str

    def render(self):
        return div(
            p(self.title),
            p(self.body),
            cls="card",
        )

print(Card(title="Ada", body="Build once, render anywhere").to_html())
```

<!-- output -->

```html
<div class="card"><p>Ada</p><p>Build once, render anywhere</p></div>
```

Continue: [Getting Started → Quickstart](getting-started/quickstart.md)
