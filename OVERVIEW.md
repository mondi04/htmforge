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

| Phase  | Contents | Status |
|--------|----------|--------|
| v0.1.0 | Core engine, 60+ HTML5 element factories, HTMX enums, framework adapters (FastAPI/Flask/Django), py.typed | ✅ Released (PyPI: 2026-03-12) |
| v0.1.2 | Bug fixes — __init_subclass__ kwargs, Page abstract guard, ruff config cleanup, importlib.metadata version | ✅ Released (PyPI: 2026-03-12) |
| v0.2.0 | DataTable, Alert, Pagination, Page, FormField, safe_html, raw(), 25 new element factories, Badge, Breadcrumb, Modal, SearchInput, hx_keyup_delay(), Component.__repr__, Alert JS-dismiss fix, Modal data-attribute fix, SearchInput API rename, mkdocs-material docs site, GitHub Actions, MIT + Commons Clause license | ✅ Released (PyPI: 2026-04-28) |
| v0.2.1 | Fix README badge links (LICENSE → absolute GitHub URL, Docs badge corrected) | ✅ Released (PyPI: 2026-04-29) |
| v0.2.2 | Documentation rewrite — component pages with props tables and rendered HTML, quickstart with full runnable examples, concepts attribute mapping table, framework guide with embedded code, contributing guide embedded, OVERVIEW + CONTRIBUTING cleaned up | ✅ Released (PyPI: 2026-04-29) |
| v0.3.0 | Spinner, Tabs, Toast, Accordion, Dropdown components; DataTable dict_rows + ColumnDef + sorting; Forms system (Form, SelectField, CheckboxField, RadioGroup, FormGroup, validation); API extensions (Element.__eq__, Component.clone(), Component.to_fragment(), render(), when()); framework adapter tests; snapshot tests | 🔜 Planned |
| v1.0.0 | Stable API guarantee, full mkdocs API reference, Django example, performance benchmarks, 100% docstring coverage | 🔜 Planned |

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

### ✅ HTML5 element factories (80+)
- All semantic elements: `div`, `span`, `p`, `h1`–`h6`, `section`, `article`, …
- Form elements: `form`, `input`, `label`, `button`, `select`, `textarea`, …
- Table elements: `table`, `thead`, `tbody`, `tr`, `th`, `td`, …
- Disclosure: `details`, `summary`
- Form grouping: `fieldset`, `legend`
- Media: `audio`, `video`, `picture`, `source`, `track`
- Interactive: `dialog`, `canvas`, `iframe`
- Semantic: `mark`, `small`, `sub`, `sup`, `kbd`, `abbr`, `time`, `address`
- Table extras: `caption`, `colgroup`, `col`
- Map: `map_`, `area`
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
| `Badge`     | `htmforge.components`               | Small inline label with variant colors       |
| `Breadcrumb`| `htmforge.components`               | Ordered nav links, aria-current support      |
| `SearchInput`| `htmforge.components`              | Text input with hx-trigger keyup debounce    |
| `Modal`     | `htmforge.components`               | Trigger button + dialog with HTMX content load |

### ✅ Quality
- **134 tests**, all green
- **mypy --strict** clean (17 source files)
- **CI** via GitHub Actions: matrix Python 3.11/3.12/3.13, pytest + mypy + ruff
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

### Block F — DataTable erweitern

**Scope:**
- `dict_rows: list[dict[str, str]] | None = None` field
- `columns: list[ColumnDef] | None = None` for label/key/sortable/width
- Sortable headers with `hx-get` + `?sort=col&dir=asc`
- Fallback to existing `rows` when `dict_rows` is None

**Acceptance criteria:**
- Tests: dict rows, missing key → empty string, sortable header renders hx-get
- mypy strict clean, ruff clean, pytest green

### Block G — Neue Komponenten

**Scope:**
- `Spinner` — `<div class="spinner spinner-{size}" role="status" aria-label="Loading">`, SpinnerSize enum (SM/MD/LG)
- `Tabs` — tab bar + panels, active tab via CSS class, HTMX lazy-load per tab
- `Toast` — timed notification, HTMX OOB-swap compatible, ToastVariant enum
- `Accordion` — `details`/`summary` based, multiple items, optional HTMX content load
- `Dropdown` — trigger button + hidden menu, HTMX toggleable

**Acceptance criteria:**
- Each component: positive test + edge case + HTMX attrs test
- Exported from `htmforge/components/__init__.py`
- Google-style docstring with usage example on every class
- mypy strict clean, ruff clean

### Block H — Forms-System

**Scope:**
- `Form` — wrapper with action, method, HTMX submit support
- `SelectField` — `<select>` with typed options list
- `CheckboxField` — single checkbox + label
- `RadioGroup` — multiple radio inputs from options list
- `FormGroup` — layout container for multiple fields
- Validation integration — accept `errors: dict[str, str]` and pass to fields

**Acceptance criteria:**
- Full test coverage per component
- Validation dict wires errors to correct fields
- mypy strict clean, ruff clean

### Block I — API-Erweiterungen

**Scope:**
- `Element.__eq__` — compare two elements by their rendered HTML
- `Component.clone(**overrides)` — return new instance with changed props
- `Component.to_fragment()` — explicit HTMX fragment method (same as to_html() but documents intent)
- `htmforge.render(component)` — top-level convenience function
- `when(condition, element)` — returns element or None for conditional rendering

**Acceptance criteria:**
- Tests for each helper
- `when()` exported from `htmforge` root
- mypy strict clean

### Block J — Testing-Infrastruktur

**Scope:**
- `tests/test_framework_adapters.py` — to_flask(), to_django() return types, auto-skip via pytest.importorskip
- Snapshot tests — rendered HTML against stored snapshots (pytest-snapshot)
- Performance benchmark — render time baseline for 1000 elements

**Acceptance criteria:**
- Framework tests skip gracefully without flask/django installed
- Snapshots stored in tests/snapshots/
- Benchmark runs with pytest --benchmark

---

## Change-Log

| Date       | Change |
|------------|--------|
| 2026-04-29 | v0.2.2: Documentation rewrite — component pages with props tables and rendered HTML, quickstart with runnable examples, concepts attribute mapping table, framework guide with embedded code, contributing guide embedded, OVERVIEW cleaned up, Roadmap extended to v0.3.0 |
| 2026-04-29 | v0.2.1: Fix README badge links (LICENSE → absolute GitHub URL, Docs badge corrected) |
| 2026-04-28 | v0.2.0: 25 new element factories, Badge, Breadcrumb, Modal, SearchInput, hx_keyup_delay(), Component.__repr__, Alert JS-dismiss fix, Modal data-attribute/script fix, SearchInput renamed fields (search_url/search_target), mkdocs-material docs site, GitHub Pages deploy workflow, GitHub Release workflow, MIT + Commons Clause license, Python 3.13 added to CI matrix |
| 2026-03-12 | v0.1.2: DataTable, Alert, Pagination, Page, FormField, safe_html(), raw(), framework adapters stable, importlib.metadata version, Pagination.hx_target optional |
| 2026-03-12 | v0.1.0: Core engine, Element, Component, 60+ HTML5 factories, HxSwap/HxTrigger/HxTarget/HxPushUrl enums, py.typed, FastAPI/Flask/Django adapters, LICENSE, CI |
| 2026-03-11 | OVERVIEW introduced as living steering document |
