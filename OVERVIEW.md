# htmforge — SDK Overview

> Type-safe, composable UI components for Python.
> Server-side rendered, HTMX-first, framework-agnostic.

This file is the **living steering document** for the project.
Rule: update it before and after every implementation block.

---

## What htmforge does

Build HTML entirely in Python — typed, composable, no templates:

```python
from htmforge import Component
from htmforge.elements import div, h1, ul, li

class UserList(Component):
    users: list[str]

    def render(self):
        return div(
            h1("Users"),
            ul(*[li(u) for u in self.users]),
            cls="container",
        )

print(UserList(users=["Ada", "Grace"]).to_html())
# <div class="container"><h1>Users</h1><ul><li>Ada</li><li>Grace</li></ul></div>
```

---

## What htmforge is not

- Not a new framework — it sits on top of FastAPI, Flask, or Django
- Not a JavaScript replacement — it uses HTMX, not a SPA framework
- Not a template language — just Python classes and functions
- Not a backend logic layer — no auth, no DB, no ORM

---

## Stack & Dependencies

| Dependency    | Purpose                       |
|---------------|-------------------------------|
| `pydantic v2` | Prop validation               |
| `markupsafe`  | Safe HTML escaping            |
| *(optional)*  | `fastapi`, `flask`, `django`  |

Core install: **2 dependencies.**

---

## Roadmap

| Phase  | Contents                                                                 | Status        |
|--------|--------------------------------------------------------------------------|---------------|
| v0.1.0 | Core engine, all HTML5 elements, HTMX enums, framework adapters          | ✅ Released   |
| v0.2.0 | DataTable, Alert, Pagination, Page, FormField, `safe_html`, `raw()`      | ✅ Released   |
| v0.3.0 | New components: Breadcrumb, Badge, Modal, SearchInput                    | 🔜 Planned    |
| v1.0.0 | Stable API, mkdocs documentation, PyPI launch                            | 🔜 Planned    |

---

## Current Status (Live)

### ✅ Core engine
- `Element` — single HTML tag, recursive `.to_html()`, `__str__` delegation
- Void elements (self-closing), attribute mapping (`cls`→`class`, `hx_get`→`hx-get`)
- XSS protection via `markupsafe.escape` on all text content
- `safe_html(text)` and `raw(text)` for unescaped trusted content

### ✅ Component system
- `Component(BaseModel, ABC)` — Pydantic v2, `validate_assignment=True`
- Abstract `render() -> Element` enforced at instantiation time
- `to_html()`, `htmx_attrs()` public API
- Framework adapters: `to_fastapi()`, `to_flask()`, `to_django()`

### ✅ HTMX integration
- Typed enums: `HxSwap`, `HxTrigger`, `HxTarget`, `HxPushUrl`
- All `hx-*` props as typed fields on every `Component`
- `htmx_attrs()` returns only set values; dicts serialized as compact JSON
- Full set of extended props: `hx_include`, `hx_vals`, `hx_headers`,
  `hx_request`, `hx_select`, `hx_select_oob`, `hx_params`, `hx_encoding`

### ✅ HTML5 element factories (60+)
- All semantic elements: `div`, `span`, `p`, `h1`–`h6`, `section`, `article`, …
- Form elements: `form`, `input`, `label`, `button`, `select`, `textarea`, …
- Table elements: `table`, `thead`, `tbody`, `tr`, `th`, `td`, …
- Document structure: `html`, `head`, `body`, `title`, `meta`, `link`,
  `script`, `style`, `noscript`
- Media: `img`, `figure`, `figcaption`, `a`, `hr`, `br`, …

### ✅ Ready-made components
| Component   | Module                              | Description                                  |
|-------------|-------------------------------------|----------------------------------------------|
| `DataTable` | `htmforge.components`               | Table with optional HTMX reload              |
| `Alert`     | `htmforge.components`               | Info/success/warning/error box, dismissible  |
| `Pagination`| `htmforge.components`               | Previous/Next + numbered pages, HTMX target  |
| `Page`      | `htmforge.components.page`          | Full HTML document (abstract), adds DOCTYPE  |
| `FormField` | `htmforge.components`               | Label + input + error div, 8 input types     |

### ✅ Quality
- **97 tests**, all green
- **mypy --strict** clean (17 source files)
- **CI** via GitHub Actions: matrix Python 3.11/3.12, pytest + mypy + ruff
- `pip install -e .` works cleanly with hatchling

---

## Definition of Done

A block is only complete when:
1. All functional scope is implemented
2. Tests added (positive + edge case per feature)
3. `pytest` green
4. `mypy htmforge/` success
5. `ruff check htmforge/` no errors
6. This OVERVIEW updated with final status

---

## Next Implementation Blocks

### Block D — New components (v0.3.0)

**Scope:**
- `Breadcrumb` — ordered nav links, HTMX-aware current-page indicator
- `Badge` — small inline label with variant colors
- `Modal` — trigger button + dialog overlay with HTMX content loading
- `SearchInput` — text input with `hx_trigger="keyup delay:300ms"` debounce

**Acceptance criteria:**
- Each component: unit tests (basic render + edge case + HTMX attrs)
- Exported from `htmforge/components/__init__.py`
- mypy strict clean, ruff clean
- Docstring with usage example on every class

### Block E — Documentation (v1.0.0)

**Scope:**
- mkdocs-material site with API reference generated from docstrings
- Getting-Started guide (5 minutes to first page)
- 3 complete example apps: FastAPI, Flask, Django
- All existing `examples/` moved into mkdocs

**Acceptance criteria:**
- `mkdocs build` exits 0 with no warnings
- API reference covers all public symbols in `htmforge/`
- Each example app is runnable with `uvicorn` / `flask run` / `python manage.py runserver`

---

## Change-Log

| Date       | Change                                                                  |
|------------|-------------------------------------------------------------------------|
| 2026-03-12 | v0.2.0: Badge, Breadcrumb, Spinner, Modal — 4 neue Komponenten          |
| 2026-03-12 | Renamed htmlkit → htmforge across entire codebase                       |
| 2026-03-12 | v0.2.0: Page, FormField, `safe_html`, `raw()`, DOCTYPE, head elements   |
| 2026-03-12 | v0.2.0: Framework adapters `to_fastapi`/`to_flask`/`to_django` stable  |
| 2026-03-12 | Bug fix: `__init_subclass__` signature corrected to `**kwargs: Any`     |
| 2026-03-12 | Bug fix: `Page` removed from `components/__init__.py` (abstract class)  |
| 2026-03-12 | Removed `.render()` from public API examples; Component usable as Element child |
| 2026-03-12 | Removed deprecated ANN101/ANN102 ruff ignores from pyproject.toml              |
| 2026-03-12 | v0.1.0: LICENSE, py.typed (PEP 561), author metadata, build + smoke test verified |
| 2026-03-12 | v0.1.0 final: importlib.metadata version, Pagination.hx_target optional, example fixes |
| 2026-03-11 | Block A–C completed: HTMX enums, framework adapters, component library  |
| 2026-03-11 | OVERVIEW introduced as living steering document                         |