# htmforge

Type-safe, composable UI components for Python that render server-side and play well with HTMX.

## Why htmforge?

- **Type-safe props**: Pydantic v2 validation on construction and assignment
- **Safe rendering**: Automatic XSS protection via markupsafe
- **HTMX-first**: Typed enums and helpers for `hx-*` attributes
- **Framework-agnostic**: Adapters for FastAPI, Flask, Django
- **20+ pre-built components**: Alerts, DataTables, Forms, Modals, Tabs, Spinners, Toasts, and more
- **Auto-error injection**: Forms automatically bind validation errors to fields
- **Snapshot testing**: Built-in regression detection via auto-created HTML snapshots
- **Performance optimized**: 1000 renders in <1 second, benchmarks included
- **Backward compatible**: Extend without breaking existing code
- **Composable**: Mix and match components with custom Elements

## Quick install

```bash
pip install htmforge
```

## Component example

```python
from htmforge import Component
from htmforge.elements import div, p, button
from htmforge.htmx import HxSwap

class Card(Component):
    title: str
    content: str
    
    def render(self):
        return div(
            p(self.title, cls="title"),
            p(self.content),
            button("Delete", hx_delete="/card/1", hx_swap=HxSwap.OUTER_HTML),
            cls="card"
        )

print(Card(title="Hello", content="World").to_html())
```

## Framework example (Flask)

```python
from flask import Flask
from htmforge.components import DataTable
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import div, h1

app = Flask(__name__)

class UsersPage(Page):
    users: list[list[str]]
    
    def _body_content(self) -> list[Element | str | None]:
        return [
            div(
                h1("Users"),
                DataTable(headers=["Name", "Email"], rows=self.users),
            )
        ]

@app.route("/users")
def users():
    rows = [["Ada Lovelace", "ada@example.com"]]
    return UsersPage(title="Users", users=rows).to_flask()

if __name__ == "__main__":
    app.run()
```

## Features

### Components (20+)

**Data Display**: Alert, Badge, Breadcrumb, DataTable (with sortable headers), Modal, Pagination, SearchInput, Toast

**Navigation & Interaction**: Accordion, Dropdown, Spinner (SM/MD/LG), Tabs

**Forms**: SelectField, CheckboxField, RadioGroup, FormGroup, Form (with auto-error injection)

**Layout**: Page (full HTML document)

### Platform

- **HTML5 Element Factories**: 80+ element functions with type-safe attributes
- **HTMX Integration**: Typed enums (HxSwap, HxTrigger, HxTarget) and helpers (hx_keyup_delay)
- **Framework Adapters**: `to_fastapi()`, `to_flask()`, `to_django()`
- **API Extensions**: Element.__eq__, Component.clone(), render(), when() helper
- **Comprehensive Testing**: 238+ unit tests, 21 snapshot tests, 5 performance benchmarks

## Continue

Start with [Concepts](getting-started/concepts.md) → [Installation](getting-started/installation.md) → [Quickstart](getting-started/quickstart.md)
