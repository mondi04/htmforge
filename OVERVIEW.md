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
- **96 tests**, all green
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
| 2026-03-12 | Renamed htmlkit → htmforge across entire codebase                       |
| 2026-03-12 | v0.2.0: Page, FormField, `safe_html`, `raw()`, DOCTYPE, head elements   |
| 2026-03-12 | v0.2.0: Framework adapters `to_fastapi`/`to_flask`/`to_django` stable  |
| 2026-03-12 | Bug fix: `__init_subclass__` signature corrected to `**kwargs: Any`     |
| 2026-03-12 | Bug fix: `Page` removed from `components/__init__.py` (abstract class)  |
| 2026-03-11 | Block A–C completed: HTMX enums, framework adapters, component library  |
| 2026-03-11 | OVERVIEW introduced as living steering document                         |


Python-Entwickler bauen Web-UIs heute mit Jinja2-Templates (keine Typsicherheit), kopieren HTMX-Attribute als rohe Strings, und haben keine wiederverwendbaren Komponenten — oder sie verlassen Python komplett und greifen zu React.

**htmforge löst das, ohne ein neues Framework zu sein.**

---

## Was htmforge kann

### 1. HTML als Python — typisiert

```python
from htmforge.elements import div, button, table, tr, td

layout = div(
    table(
        tr(td("Alice"), td("alice@example.com")),
        tr(td("Bob"),   td("bob@example.com")),
    ),
    cls="container"
)

print(layout.to_html())
```

Kein Template, kein String-Concat. Nur Python — mit IDE-Autocompletion und Typ-Prüfung.

---

### 2. Komponenten mit typisierten Props

```python
from htmforge import Component
from htmforge.elements import table, tr, td

class UserTable(Component):
    users: list[User]          # Pydantic-validiert
    show_email: bool = True

    def render(self):
        return table(
            *[tr(td(u.name), td(u.email) if self.show_email else None)
              for u in self.users]
        )
```

Props werden wie Pydantic-Modelle deklariert — Validierung, Defaults und IDE-Support inklusive.

---

### 3. HTMX first-class

```python
from htmforge import Component
from htmforge.elements import button
from htmforge.htmx import HxSwap

class DeleteButton(Component):
    user_id: int
    hx_swap: HxSwap = HxSwap.OUTER_HTML   # typisiertes Enum

    def render(self):
        return button(
            "Löschen",
            hx_delete=f"/users/{self.user_id}",
            hx_swap=self.hx_swap,
            hx_confirm="Wirklich löschen?",
        )
```

Alle HTMX-Attribute (`hx_get`, `hx_post`, `hx_trigger`, `hx_target`, ...) sind typisierte Felder — kein String-Raten mehr.

---

### 4. Framework-agnostisch

```python
# FastAPI
@app.get("/users")
def users_page():
    return UserTable(users=db_users).to_fastapi()

# Flask
@app.route("/users")
def users_page():
    return UserTable(users=db_users).to_flask()

# Django
def users_page(request):
    return UserTable(users=db_users).to_django()
```

Ein Adapter-Einzeiler — fertig.

---

### 5. Fertige Komponenten (ab v0.2)

Sofort verwendbar, anpassbar, composable:

| Komponente     | Beschreibung                              |
|----------------|-------------------------------------------|
| `DataTable`    | Sortierbar, paginiert, HTMX-basiert       |
| `SearchInput`  | Live-Suche mit Debounce via HTMX          |
| `Modal`        | Trigger + Content als eine Komponente     |
| `Toast`        | Benachrichtigungen, auto-dismiss          |
| `Form`         | Validierungs-Feedback, Pydantic-gebunden  |
| `Sidebar`      | Navigations-Layout                        |
| `Navbar`       | Responsive Header                         |
| `Pagination`   | HTMX-basiertes Blättern                   |

---

## Was htmforge nicht ist

- **Kein neues Framework** — es liegt über FastAPI, Flask oder Django
- **Kein JavaScript-Ersatz** — es nutzt HTMX, ersetzt aber kein SPA-Framework
- **Keine eigene Template-Sprache** — nur Python-Klassen und -Funktionen
- **Kein Backend-Logic-Layer** — keine Auth, keine DB, keine ORM

---

## Stack & Abhängigkeiten

| Dependency     | Zweck                        |
|----------------|------------------------------|
| `pydantic v2`  | Props-Validierung            |
| `markupsafe`   | Sicheres HTML-Escaping       |
| *(optional)*   | `fastapi`, `flask`, `django` |

Kern-Install: **2 Dependencies.**

---

## Lizenz & Open Source

MIT — kostenlos, für immer, für alle.  
Monorepo auf GitHub, Contributions willkommen.

---

## Roadmap

| Phase | Inhalt                              | Ziel         | Status |
|-------|-------------------------------------|--------------|--------|
| v0.1  | HTML-Primitives, Component-Klasse   | Woche 4      | Aktiv |
| v0.2  | HTMX-Integration, Framework-Adapter | Woche 8      | Geplant |
| v0.3  | Fertige Komponenten-Library         | Woche 12     | Geplant |
| v1.0  | Stabile API, vollständige Docs      | Monat 4      | Geplant |

---

## Entwicklungsmodus (Overview-Driven)

Diese Datei ist die **verbindliche Arbeitsgrundlage**.

Regel:
- Erst diese Overview aktualisieren (Ziel, Scope, Akzeptanzkriterien)
- Danach exakt nach dem neuen Abschnitt implementieren
- Nach Abschluss den Status hier aktualisieren

Damit ist immer klar:
- Was als Nächstes gebaut wird
- Wann ein Schritt als "fertig" gilt
- Welche Tests den Abschluss belegen

---

## Aktueller Stand (Live)

### Bereits umgesetzt

- Core-Bausteine für `Element` und `Component`
- HTML-Rendering mit Escaping via `markupsafe`
- Attribut-Mapping für `cls`, `for_`, `hx_*`
- Public Exports im Package-Root
- Erste Element-Factories und Testbasis

### Qualitäts-Gates

- `pytest` muss grün sein
- `mypy --strict` muss ohne Fehler laufen
- Keine neuen Core-Dependencies außer `pydantic` und `markupsafe`

---

## Nächste Implementierungsblöcke (in Reihenfolge)

### Block A — HTMX-Typisierung vervollständigen (Abgeschlossen)

Scope:
- `HxSwap`, `HxTrigger` konsolidieren/ergänzen
- klare Nutzbarkeit in Component-Props

Fortschritt (2026-03-11):
- Enum-Rendering in HTML stabilisiert (`Enum` -> `.value`)
- Typisierte HTMX-Basisprops in `Component` ergänzt
- `htmx_attrs()` Helper für direkte Nutzung in `render()` ergänzt
- Erweiterte HTMX-Props (`hx_headers`, `hx_request`, `hx_select`, `hx_select_oob`, `hx_params`, `hx_encoding`) ergänzt
- Strukturierte HTMX-Werte (Dict) werden in `htmx_attrs()` als JSON normalisiert

Akzeptanzkriterien:
- Typed Props mit HTMX-Enums laufen in Beispielen ohne Workarounds
- Tests für typische HTMX-Attribute vorhanden

### Block B — Framework-Adapter stabilisieren

Status:
- Nächster aktiver Block

Scope:
- FastAPI/Flask/Django Adapter robust dokumentieren
- klare Fehlermeldungen bei fehlenden optionalen Dependencies

Akzeptanzkriterien:
- Adapter-Rückgabetypen und Verhalten testbar
- Keine Änderung am Core-Dependency-Footprint

### Block C — Erste produktive Komponenten

Scope:
- `DataTable`, `SearchInput`, `Pagination` als Startset
- SSR + HTMX-first Verhalten

Akzeptanzkriterien:
- Jede Komponente mit Unit-Tests
- Beispiele in Doku lauffähig

---

## Definition of Done pro Block

Ein Block ist nur fertig, wenn:
- Funktionaler Scope umgesetzt ist
- Tests ergänzt wurden
- `pytest` grün ist
- `mypy --strict` grün ist
- Diese Overview mit finalem Status aktualisiert wurde

---

## Change-Log (kurz)

- 2026-03-11: Overview als lebendes Steuerdokument eingeführt
- 2026-03-11: Reihenfolge A/B/C und DoD verbindlich ergänzt
- 2026-03-11: Block A gestartet, HTMX-Enum-Rendering als Kernverhalten festgelegt
- 2026-03-11: Block A erweitert um typisierte HTMX-Component-Props und `htmx_attrs()`
- 2026-03-11: Block A abgeschlossen, inklusive erweiterter HTMX-Props und JSON-Normalisierung