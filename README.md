<!-- badges -->
[![PyPI version](https://img.shields.io/pypi/v/htmforge.svg)](https://pypi.org/project/htmforge/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT + Commons Clause](https://img.shields.io/badge/License-MIT%20%2B%20Commons%20Clause-blue.svg)](https://github.com/mondi04/htmforge/blob/main/LICENSE)
[![mypy strict](https://img.shields.io/badge/mypy-strict-brightgreen.svg)](https://mypy.readthedocs.io/)
[![CI](https://github.com/mondi04/htmforge/actions/workflows/ci.yml/badge.svg)](https://github.com/mondi04/htmforge/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mondi04.github.io%2Fhtmforge-orange.svg)](https://mondi04.github.io/htmforge/)

# htmforge

Type-safe, composable UI components for Python. Server-side rendered,
HTMX-first, framework-agnostic.

## Why htmforge?

- Type-safe props via Pydantic v2: props are validated on construction and
  on assignment.
- Small Element primitives with safe rendering: `Element.to_html()`
  escapes text and maps Python attrs to HTML (e.g. `cls`→`class`).
- First-class HTMX support: typed enums and helpers for `hx-*` attrs.
- Framework adapters: `to_fastapi()`, `to_flask()`, `to_django()` on
  components for easy integration.

## Installation

```bash
pip install htmforge
```

## Quickstart (Flask)

Copy-pasteable minimal Flask example using a `Page` and a `DataTable`.

```python
from flask import Flask

from htmforge.components.page import Page
from htmforge.components import DataTable
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
    app.run(debug=True)
```

## Elements

`htmforge.elements` exposes small factory functions for HTML tags. These
map Pythonic attribute names to HTML and escape text safely. Example:

```python
from htmforge.elements import div, span, input

el = div(
    span("Name:"),
    input(type="search", name="q", hx_get="/search", cls="search"),
    cls="form-row",
)
print(el.to_html())
```

The `hx_get` argument renders as `hx-get`, and text is escaped by
default to prevent XSS.

## Components

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

## HTMX integration

Typed enums live in `htmforge.htmx`: `HxSwap`, `HxTrigger`, `HxTarget`,
and `HxPushUrl`. They render the correct attribute values. Example:

```python
from htmforge.elements import button
from htmforge.htmx import HxSwap, HxTarget

btn = button(
    "Delete",
    hx_delete="/items/1",
    hx_swap=HxSwap.OUTER_HTML,
    hx_target=HxTarget.CLOSEST_TR,
)
```

Use `hx_keyup_delay(ms)` to produce `keyup delay:{ms}ms` trigger strings
for debounced search inputs.

## Framework support

FastAPI example:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    return UsersPage(title="Home").to_html()
```

Flask example (adapter shown above uses `to_flask()`):

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return UsersPage(title="Home").to_flask()
```

Django example:

```python
def index(request):
    return UsersPage(title="Home").to_django()
```

## License

This project is licensed under the MIT License with the Commons Clause
condition. It is free for personal projects, open source projects, and
small businesses (see `LICENSE`). Organizations with annual revenue or
funding over USD 1,000,000 or more than 100 employees require a
separate commercial license from the author.

## Contributing

See `CONTRIBUTING.md` and the docs site at
https://mondi04.github.io/htmforge/ for contribution guidelines.

