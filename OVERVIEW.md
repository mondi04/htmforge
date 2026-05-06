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
| v0.2.0 | DataTable, Alert, Pagination, Page, FormField, safe_html, raw(), 25 new element factories (dialog, details, audio, video, picture, canvas, iframe, meter, progress, kbd, abbr, time, address, mark, small, sub, sup, caption, colgroup, col, source, track, map_, area), Badge, Breadcrumb, Modal, SearchInput, hx_keyup_delay(), Component.__repr__, Alert JS-dismiss fix, Modal data-attribute fix, SearchInput API rename (search_url/search_target), mkdocs-material documentation site, GitHub Actions (CI Python 3.13, docs deploy, release workflow), MIT + Commons Clause license | ✅ Released (PyPI: 2026-04-28) |
| v0.2.1 | Fix README badge links (LICENSE → GitHub, Docs → GitHub repo) | ✅ Released (PyPI: 2026-04-29) |
| v0.2.2 | Documentation rewrite — component pages with props tables and rendered HTML, quickstart with full runnable examples, concepts attribute mapping table, framework guide with embedded code, contributing guide embedded, OVERVIEW + CONTRIBUTING cleaned up | ✅ Released (PyPI: 2026-04-29) |
| v0.3.0 | **Block F**: DataTable dict_rows + ColumnDef + sortable headers. **Block G**: Spinner, Tabs, Toast, Accordion, Dropdown. **Block H**: SelectField, CheckboxField, RadioGroup, FormGroup, Form (auto-error injection). **Block I**: Element.__eq__/__hash__, Component.clone(), to_fragment(), render(), when(). **Block J**: Framework adapters (FastAPI/Flask/Django), snapshot tests (21), performance benchmarks (5). **Result**: 238 tests passing, mypy strict, ruff clean. | ✅ Released (PyPI: 2026-05-06) |
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
| `DataTable` | `htmforge.components`               | Table with dict/list rows, sortable headers, HTMX reload |
| `Alert`     | `htmforge.components`               | Info/success/warning/error box, dismissible  |
| `Pagination`| `htmforge.components`               | Previous/Next + numbered pages, HTMX target  |
| `Page`      | `htmforge.components.page`          | Full HTML document (abstract), adds DOCTYPE  |
| `FormField` | `htmforge.components`               | Label + input + error div, 8 input types     |
| `Badge`     | `htmforge.components`               | Small inline label with variant colors       |
| `Breadcrumb`| `htmforge.components`               | Ordered nav links, aria-current support      |
| `SearchInput`| `htmforge.components`              | Text input with hx-trigger keyup debounce    |
| `Modal`     | `htmforge.components`               | Trigger button + dialog with HTMX content load |
| `Spinner`   | `htmforge.components`               | Accessible loading indicator (SM/MD/LG)      |
| `Tabs`      | `htmforge.components`               | Tab navigation with HTMX lazy-load           |
| `Toast`     | `htmforge.components`               | Timed notifications with OOB swap            |
| `Accordion` | `htmforge.components`               | Collapsible sections (details/summary)       |
| `Dropdown`  | `htmforge.components`               | Trigger button with menu items, toggle       |
| `SelectField` | `htmforge.components`             | Dropdown select with options                 |
| `CheckboxField` | `htmforge.components`           | Single checkbox with label and error         |
| `RadioGroup` | `htmforge.components`              | Radio button group with legend               |
| `FormGroup` | `htmforge.components`               | Container for multiple form fields           |
| `Form`      | `htmforge.components`               | Full form with auto-error injection, HTMX    |

### ✅ Quality
- **238 tests**, all passing (+ 5 skipped framework adapters)
- **mypy --strict** clean (22 source files)
- **ruff** lint and format clean
- **Snapshot tests**: 21 regression tests auto-created on first run
- **Performance**: 1000 renders <1s for elements, <2s for DataTable
- **CI** via GitHub Actions: matrix Python 3.11/3.12/3.13, pytest + mypy + ruff
- **Framework adapters**: FastAPI, Flask, Django (optional, skip if not installed)
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

## Implementation Blocks (v0.3.0 — Completed ✅)

### Block F — DataTable erweitert

**Scope:**
- `ColumnDef` class: key, label, sortable, width fields
- dict_rows support: render from list[dict[str, str]]
- Sortable headers: ColumnDef.sortable renders hx-get links
- Sort tracking: sort_url, current_sort, sort_dir for direction flip
- Full backwards compatibility with rows: list[list[str]]

**Status:** ✅ Complete — 7 tests passing

### Block G — Neue Komponenten

**Scope:**
- `Spinner` with SpinnerSize enum (SM/MD/LG), role/aria-label
- `Tabs` with HTMX lazy-load per inactive tab, active state
- `Toast` with ToastVariant, hx-swap-oob, auto-dismiss duration
- `Accordion` based on details/summary, open_index control
- `Dropdown` with trigger button, HTMX toggle, menu items

**Status:** ✅ Complete — 25 component tests passing

### Block H — Forms-System

**Scope:**
- `SelectField` — dropdown with typed options, error support
- `CheckboxField` — single checkbox with label
- `RadioGroup` — fieldset with multiple radio inputs
- `FormGroup` — layout container for multiple fields
- `Form` — wrapper with auto error injection, HTMX submit

**Status:** ✅ Complete — 22 form tests passing

### Block I — API-Erweiterungen

**Scope:**
- `Element.__eq__` and `__hash__` — compare by rendered HTML
- `Component.clone(**overrides)` — new instance with changed props
- `Component.to_fragment()` — explicit HTMX fragment method
- `htmforge.render()` — top-level convenience function
- `htmforge.when()` — conditional rendering helper

**Status:** ✅ Complete — All API methods working

### Block J — Testing-Infrastruktur

**Scope:**
- `tests/test_framework_adapters.py` — FastAPI/Flask/Django with auto-skip
- `tests/test_snapshots.py` — 21 HTML regression tests
- `tests/test_performance.py` — 5 benchmarks all <1-2s for 1000 renders
- `tests/snapshots/` directory added to .gitignore
- Machine-generated snapshots auto-created on first run

**Status:** ✅ Complete — 238 tests passing, 5 skipped (Django optional)

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
| 2026-05-06 | v0.3.0 Complete: **Block F** (DataTable dict_rows, ColumnDef, sortable headers, backwards-compatible). **Block G** (Spinner SM/MD/LG, Tabs HTMX lazy-load, Toast OOB swap, Accordion details/summary, Dropdown HTMX toggle). **Block H** (SelectField, CheckboxField, RadioGroup, FormGroup, Form with auto-error injection). **Block I** (Element.__eq__/__hash__, Component.clone(), to_fragment(), render(), when() helpers). **Block J** (Framework adapters FastAPI/Flask/Django, 21 snapshot regression tests, 5 performance benchmarks). **Result**: 238 tests passing, 5 skipped (Django), mypy strict clean, ruff clean, full documentation updated. |
| 2026-04-29 | v0.2.2: Documentation rewrite — component pages with props tables and rendered HTML, quickstart with runnable examples, concepts attribute mapping table, framework guide with embedded code, contributing guide embedded, OVERVIEW cleaned up, Roadmap extended to v0.3.0 |
| 2026-04-29 | v0.2.1: Fix README badge links — LICENSE und Docs-Badge zeigen auf korrekte URLs |
| 2026-04-28 | v0.2.0: 25 new element factories, Badge, Breadcrumb, Modal, SearchInput, hx_keyup_delay(), Component.__repr__, Alert JS-dismiss fix, Modal data-attribute/script fix, SearchInput renamed fields (search_url/search_target), mkdocs-material docs site, GitHub Pages deploy workflow, GitHub Release workflow, MIT + Commons Clause license, Python 3.13 added to CI matrix |
| 2026-03-12 | v0.1.2: DataTable, Alert, Pagination, Page, FormField, safe_html(), raw(), framework adapters stable, importlib.metadata version, Pagination.hx_target optional |
| 2026-03-12 | v0.1.0: Core engine, Element, Component, 60+ HTML5 factories, HxSwap/HxTrigger/HxTarget/HxPushUrl enums, py.typed, FastAPI/Flask/Django adapters, LICENSE, CI |
| 2026-03-11 | OVERVIEW introduced as living steering document |
