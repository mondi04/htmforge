# htmforge

Type-safe, composable UI components for Python - server-side rendered, HTMX-first.

## Why htmforge?

- **Type-safe props**: Pydantic v2 validation on construction and assignment.
- **Safe rendering**: Automatic XSS protection via `markupsafe`.
- **HTMX-first**: Typed enums and helpers for `hx-*` attributes.
- **Framework-agnostic**: Adapters for FastAPI, Flask, Django.
- **20+ pre-built components**: Alert, Badge, Breadcrumb, DataTable, Page, Pagination, SearchInput, Spinner, Tabs, Toast, Accordion, Dropdown, SelectField, CheckboxField, RadioGroup, FormGroup, and Form.
- **Auto-error injection**: Forms automatically bind validation errors to fields.
- **Snapshot testing**: Built-in regression detection via auto-created HTML snapshots.
- **Performance optimized**: 1000 renders in under 1 second for core element paths.
- **Backward compatible**: Extend without breaking existing code.
- **Composable**: Mix and match components with custom Elements.

## Quick install

```bash
pip install htmforge
```

## Component example

```python
from htmforge import Component
from htmforge.elements import button, div, p
from htmforge.htmx import HxSwap

class Card(Component):
    title: str
    content: str

    def render(self):
        return div(
            p(self.title, cls="title"),
            p(self.content),
            button("Delete", hx_delete="/card/1", hx_swap=HxSwap.OUTER_HTML),
            cls="card",
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

**Layout & Structure**: Page

**Data Display**: Alert, Badge, Breadcrumb, DataTable, Pagination, Toast

**Navigation & Interaction**: Accordion, Dropdown, Modal, SearchInput, Spinner, Tabs

**Forms**: FormField, SelectField, CheckboxField, RadioGroup, FormGroup, Form

### Platform

- **80+ HTML5 element factories** with automatic attribute mapping and XSS protection
- **20+ pre-built components**: Alerts, DataTables, Forms, Modals, Spinners, Tabs, Toasts, and more
- **Typed HTMX attributes** via enums — `HxSwap`, `HxTarget`, `HxTrigger`, `HxPushUrl`
- **Framework adapters** for FastAPI, Flask, and Django
- **Auto-error injection** in Form — validation errors routed to fields automatically
- **py.typed** — full mypy strict and pyright support

- **`Component.to_json()`** — returns `{"html": ..., "component": ...}` for use in API endpoints
- **`Page.lang`** — sets the `lang` attribute on the `<html>` element for accessibility

## Continue

Start with [Concepts](getting-started/concepts.md) -> [Installation](getting-started/installation.md) -> [Quickstart](getting-started/quickstart.md)
