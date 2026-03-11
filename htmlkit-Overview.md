# htmlkit — SDK Overview

> Typsichere, composable UI-Komponenten für Python. Server-side rendered, framework-agnostisch, HTMX-ready.

---

## Das Problem

Python-Entwickler bauen Web-UIs heute mit Jinja2-Templates (keine Typsicherheit), kopieren HTMX-Attribute als rohe Strings, und haben keine wiederverwendbaren Komponenten — oder sie verlassen Python komplett und greifen zu React.

**htmlkit löst das, ohne ein neues Framework zu sein.**

---

## Was htmlkit kann

### 1. HTML als Python — typisiert

```python
from htmlkit.elements import div, button, table, tr, td

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
from htmlkit import Component
from htmlkit.elements import table, tr, td

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
from htmlkit import Component
from htmlkit.elements import button
from htmlkit.htmx import HxSwap

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

## Was htmlkit nicht ist

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

| Phase | Inhalt                              | Ziel         |
|-------|-------------------------------------|--------------|
| v0.1  | HTML-Primitives, Component-Klasse   | Woche 4      |
| v0.2  | HTMX-Integration, Framework-Adapter | Woche 8      |
| v0.3  | Fertige Komponenten-Library         | Woche 12     |
| v1.0  | Stabile API, vollständige Docs      | Monat 4      |