# htmforge

[![PyPI version](https://img.shields.io/pypi/v/htmforge.svg)](https://pypi.org/project/htmforge/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT + Commons Clause](https://img.shields.io/badge/License-MIT%20%2B%20Commons%20Clause-blue.svg)](https://github.com/mondi04/htmforge/blob/main/LICENSE)
[![mypy strict](https://img.shields.io/badge/mypy-strict-brightgreen.svg)](https://mypy.readthedocs.io/)
[![CI](https://github.com/mondi04/htmforge/actions/workflows/ci.yml/badge.svg)](https://github.com/mondi04/htmforge/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mondi04.github.io%2Fhtmforge-orange.svg)](https://mondi04.github.io/htmforge/)

**Type-safe, composable HTML components for Python — server-side rendered, HTMX-first, framework-agnostic.**

Build HTML entirely in Python. No templates, no string formatting, no XSS surprises.
Validated props via Pydantic, typed HTMX attributes, and direct adapters for FastAPI, Flask, and Django.

---

## What you can build with htmforge

A full user admin panel — live search, modals, forms with validation, pagination, toasts — **in pure Python, no templates**:

> 📁 **[See the full working demo →](examples/admin-panel/)** — clone it, run it in 30 seconds.

```python
# A complete, interactive page in ~20 lines of Python
class UsersPage(BaseAdminPage):
    users: list[dict]
    total: int
    page: int

    def _body_content(self):
        return [
            SearchInput(name="q", hx_get="/users/search", hx_target="#user-table"),
            DataTable(
                id="user-table",
                columns=[ColumnDef("name", "Name"), ColumnDef("email", "Email"), ColumnDef("role", "Role")],
                rows=self.users,
            ),
            Pagination(current=self.page, total_pages=ceil(self.total / 5), hx_target="#user-table"),
        ]
```

---

## Why htmforge?

```python
# ❌ Before — string templates, no type safety, easy to get wrong
html = f'<div class="alert {variant}"><p>{message}</p></div>'

# ✅ After — validated props, typed attributes, XSS-safe by default
Alert(variant=AlertVariant.SUCCESS, content=message).to_html()
```

**Compared to the alternatives:**

| | htmforge | Jinja2 templates | `dominate` | `htpy` |
|---|---|---|---|---|
| Type-safe props | ✅ Pydantic v2 | ❌ | ❌ | ❌ |
| Validated on assignment | ✅ | ❌ | ❌ | ❌ |
| XSS protection | ✅ built-in | ⚠️ manual | ⚠️ partial | ✅ |
| HTMX typed enums | ✅ | ❌ | ❌ | ❌ |
| Pre-built components | ✅ 20+ | ❌ | ❌ | ❌ |
| Framework adapters | ✅ | ✅ | ❌ | ❌ |
| py.typed / mypy strict | ✅ | ❌ | ❌ | ⚠️ partial |

- **Type-safe props** via Pydantic v2 — validated on construction *and* assignment
- **XSS protection** built-in — `markupsafe` escapes all text content automatically
- **HTMX-native** — typed enums for every `hx-*` attribute, no string guessing
- **20+ pre-built components** — Alerts, DataTables, Forms, Modals, Spinners, Tabs, and more
- **Framework adapters** — `to_fastapi()`, `to_flask()`, `to_django()` out of the box
- **2 dependencies** — only `pydantic` and `markupsafe`; FastAPI/Flask/Django are optional
- **py.typed** — full inline type stubs, works perfectly with mypy strict and pyright

---

## Installation

```bash
pip install htmforge
```

Requires Python 3.11+. No extra dependencies for core usage.

---

## 60-second example

```python
from htmforge import Component
from htmforge.elements import div, h1, p

class UserCard(Component):
    name: str
    email: str

    def render(self):
        return div(
            h1(self.name),
            p(self.email, cls="text-muted"),
            cls="card",
        )

print(UserCard(name="Ada Lovelace", email="ada@example.com").to_html())
# <div class="card"><h1>Ada Lovelace</h1><p class="text-muted">ada@example.com</p></div>
```

---

## Pre-built Components

htmforge ships with 20+ production-ready components, all with typed props and HTMX support.

### Layout & Structure

| Component | Description | Import |
|-----------|-------------|--------|
| `Page` | Abstract full-page component — emits `<!DOCTYPE html>` | `from htmforge.components.page import Page` |

### Data Display

| Component | Description | Import |
|-----------|-------------|--------|
| `Alert` | Info / success / warning / error box, dismissible | `from htmforge.components import Alert` |
| `Badge` | Small inline label with variant colors | `from htmforge.components import Badge` |
| `Breadcrumb` | Ordered nav with `aria-current` for active item | `from htmforge.components import Breadcrumb` |
| `DataTable` | List/dict rows, sortable headers, HTMX reload | `from htmforge.components import DataTable, ColumnDef` |
| `Pagination` | Previous/Next + numbered page links, HTMX target | `from htmforge.components import Pagination` |
| `Toast` | Timed notifications with OOB swap support | `from htmforge.components import Toast` |

### Navigation & Interaction

| Component | Description | Import |
|-----------|-------------|--------|
| `Accordion` | Collapsible sections using `<details>`/`<summary>` | `from htmforge.components import Accordion` |
| `Dropdown` | Trigger button with HTMX-toggled menu | `from htmforge.components import Dropdown` |
| `Modal` | Trigger button + `<dialog>` overlay, HTMX-loaded body | `from htmforge.components import Modal` |
| `SearchInput` | Text input with `keyup` debounce via HTMX | `from htmforge.components import SearchInput` |
| `Spinner` | Accessible loading indicator (SM / MD / LG) | `from htmforge.components import Spinner, SpinnerSize` |
| `Tabs` | Tab strip with HTMX lazy-load per inactive tab | `from htmforge.components import Tabs` |

### Forms & Input

| Component | Description | Import |
|-----------|-------------|--------|
| `Form` | Full form with **auto-error injection** and HTMX submit | `from htmforge.components import Form` |
| `FormField` | Label + input + optional error block, 8 input types | `from htmforge.components import FormField, InputType` |
| `CheckboxField` | Single checkbox with label and error display | `from htmforge.components import CheckboxField` |
| `SelectField` | Dropdown `<select>` with typed options | `from htmforge.components import SelectField` |
| `RadioGroup` | Radio button group with `<fieldset>` and legend | `from htmforge.components import RadioGroup` |
| `FormGroup` | Layout container for multiple form fields | `from htmforge.components import FormGroup` |

---

## HTMX Integration

Every `hx-*` attribute is a typed enum — no misspelled strings, full IDE autocompletion.

```python
from htmforge.elements import button, input
from htmforge.htmx import HxSwap, HxTarget, hx_keyup_delay

# Delete button with confirmation
btn = button(
    "Delete",
    hx_delete="/items/1",
    hx_swap=HxSwap.OUTER_HTML,
    hx_target=HxTarget.CLOSEST_TR,
    hx_confirm="Really delete this item?",
)
# → <button hx-delete="/items/1" hx-swap="outerHTML"
#           hx-target="closest tr" hx-confirm="Really delete this item?">Delete</button>

# Debounced search input
search = input(
    type="search",
    name="q",
    hx_get="/search",
    hx_trigger=hx_keyup_delay(300),   # → "keyup delay:300ms"
    hx_target="#results",
    placeholder="Search...",
)
```

Available enums: `HxSwap`, `HxTrigger`, `HxTarget`, `HxPushUrl`

---

## Framework Adapters

### FastAPI

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from htmforge.components.page import Page
from htmforge.elements import div, h1

app = FastAPI()

class HomePage(Page):
    def _body_content(self):
        return [div(h1("Hello from htmforge"))]

@app.get("/", response_class=HTMLResponse)
def index():
    return HomePage(title="Home").to_html()
```

### Flask

```python
from flask import Flask
from htmforge.components.page import Page
from htmforge.elements import div, h1

app = Flask(__name__)

class HomePage(Page):
    def _body_content(self):
        return [div(h1("Hello from htmforge"))]

@app.route("/")
def index():
    return HomePage(title="Home").to_flask()  # Returns Flask Response directly
```

### Django

```python
from htmforge.components.page import Page
from htmforge.elements import div, h1

class HomePage(Page):
    def _body_content(self):
        return [div(h1("Hello from htmforge"))]

def index(request):
    return HomePage(title="Home").to_django()  # Returns HttpResponse directly
```

---

## Form with Validation Errors

The `Form` component automatically routes validation errors to the matching field by name:

```python
from htmforge.components import Form, FormField, InputType

form = Form(
    action="/register",
    fields=[
        FormField(name="username", label_text="Username", input_type=InputType.TEXT),
        FormField(name="email",    label_text="Email",    input_type=InputType.EMAIL),
    ],
    errors={
        "email": "This email is already registered.",
    },
    submit_label="Create Account",
)
# The email field automatically renders its error block — no manual wiring needed.
```

---

## Elements

`htmforge.elements` provides factory functions for all 80+ HTML5 elements. Python attribute names are mapped automatically:

| Python | HTML output |
|--------|-------------|
| `cls="btn"` | `class="btn"` |
| `hx_get="/url"` | `hx-get="/url"` |
| `data_id="1"` | `data-id="1"` |
| `required=True` | `required` (boolean flag) |
| `disabled=False` | *(omitted)* |

```python
from htmforge.elements import form, input, button, label

el = form(
    label("Search", for_="q"),
    input(id="q", type="search", name="q", hx_get="/search", hx_target="#results"),
    button("Go", type="submit"),
    cls="search-form",
    hx_boost="true",
)
```

All text content is escaped by `markupsafe` — safe by default, opt-out with `safe_html()` or `raw()` for trusted content.

---

## API Helpers

```python
from htmforge import render, when
from htmforge.elements import div, p

# render() — top-level convenience, works on Element or Component
html: str = render(div(p("Hello")))

# when() — conditional rendering, returns element or None
content = when(user.is_admin, admin_panel)
```

`Component.clone(**overrides)` creates a new instance with changed props without mutating the original:

```python
base = Alert(variant=AlertVariant.INFO, content="Default message")
success = base.clone(variant=AlertVariant.SUCCESS, content="Saved!")
```

---

## Quality & Testing

htmforge is built for production:

```
238 tests passing  ·  mypy --strict clean  ·  ruff lint + format clean  ·  CI on Python 3.11 / 3.12 / 3.13
```

- **Unit tests** — render logic, HTMX attributes, edge cases for all components
- **Snapshot tests** (21) — HTML regression detection, auto-generated on first run
- **Performance benchmarks** — 1 000 renders of elements <1s, DataTable <2s
- **Framework adapter tests** — FastAPI, Flask, Django with graceful skip if not installed

```bash
pytest                          # all tests
pytest -v                       # verbose
mypy htmforge/ --strict         # type check
ruff check htmforge/            # lint
ruff format --check htmforge/   # format check
```

---

## What htmforge is not

- **Not a new framework** — sits on top of FastAPI, Flask, or Django
- **Not a JavaScript replacement** — uses HTMX, not a SPA approach
- **Not a template language** — pure Python classes and functions
- **Not a backend layer** — no auth, no ORM, no routing

---

## License

MIT License with the [Commons Clause](https://commonsclause.com/) condition.

Free for personal projects, open-source projects, and small businesses.
Organizations with **annual revenue or funding over USD 1 000 000** or **more than 100 employees** require a separate commercial license — contact the author.

See [`LICENSE`](LICENSE) for the full text.

---

## Contributing

Contributions are welcome! Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup instructions, coding standards, and the commit convention. The full docs are at [mondi04.github.io/htmforge](https://mondi04.github.io/htmforge/).