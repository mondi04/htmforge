<!-- badges -->
[![PyPI version](https://img.shields.io/pypi/v/htmlkit.svg)](https://pypi.org/project/htmlkit/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![mypy strict](https://img.shields.io/badge/mypy-strict-brightgreen.svg)](https://mypy.readthedocs.io/)

# htmlkit

Type-safe, composable UI components for Python — server-side rendered, HTMX-first, framework-agnostic.

## Why htmlkit?

- **No templates** — build HTML with plain Python classes and type-checked props
- **HTMX-native** — typed enums for every `hx-*` attribute, zero string guessing
- **Pydantic validation** — props are validated on construction and assignment
- **Framework-agnostic** — works with FastAPI, Flask, Django, or any WSGI/ASGI app

## Installation

```bash
pip install htmlkit
```

## Quickstart

A FastAPI route that renders a full page with a user table and an add-user form:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from htmlkit.components.page import Page
from htmlkit.components import DataTable, FormField, InputType
from htmlkit.core.element import Element
from htmlkit.elements import div, h1

app = FastAPI()

USERS = [["Ada Lovelace", "ada@example.com"], ["Grace Hopper", "grace@example.com"]]


class UsersPage(Page):
    users: list[list[str]]
    added: bool = False

    def _body_content(self) -> list[Element | str | None]:
        table = DataTable(
            headers=["Name", "Email"],
            rows=self.users,
        )
        form = FormField(
            name="name",
            label_text="Full Name",
            input_type=InputType.TEXT,
            required=True,
        )
        return [
            div(
                h1("Users"),
                table.render(),
                form.render(),
            )
        ]


@app.get("/users", response_class=HTMLResponse)
def list_users() -> str:
    return UsersPage(
        title="Users",
        css_urls=["/static/style.css"],
        users=USERS,
    ).to_html()
```

## Components

| Component   | Description                                    | Import                                  |
|-------------|------------------------------------------------|-----------------------------------------|
| `DataTable` | Table with optional HTMX reload                | `from htmlkit.components import DataTable` |
| `Alert`     | Info/success/warning/error box, dismissible    | `from htmlkit.components import Alert`  |
| `Pagination`| Previous/Next + page links with HTMX targeting | `from htmlkit.components import Pagination` |
| `Page`      | Full HTML document with DOCTYPE, abstract base | `from htmlkit.components.page import Page` |
| `FormField` | Label + input + error div, 8 input types       | `from htmlkit.components import FormField` |

## HTMX Integration

All HTMX attributes are available as typed enums — no string typos:

```python
from htmlkit.elements import button
from htmlkit.htmx import HxSwap, HxTarget, HxTrigger

btn = button(
    "Delete",
    hx_delete="/users/1",
    hx_swap=HxSwap.OUTER_HTML,
    hx_target=HxTarget.CLOSEST_TR,
    hx_confirm="Really delete?",
)
# → <button hx-delete="/users/1" hx-swap="outerHTML"
#           hx-target="closest tr" hx-confirm="Really delete?">Delete</button>
```

## Framework Support

**FastAPI**
```python
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return MyPage(title="Home").to_html()
```

**Flask**
```python
from flask import Response

@app.route("/")
def index() -> Response:
    return MyPage(title="Home").to_flask()
```

**Django**
```python
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest) -> HttpResponse:
    return MyPage(title="Home").to_django()
```

## Contributing

Contributions are welcome — please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

MIT — see [LICENSE](LICENSE).
