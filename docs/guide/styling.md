# Styling

htmforge generiert nur HTML-Struktur und feste CSS-Klassennamen (z.B. `alert alert-success`).
**Das Core-Package liefert kein CSS aus.** Du bringst dein eigenes Stylesheet mit oder
nutzt das optionale Default-Theme unten.

## Optionales Default-Theme

Ein fertiges Stylesheet für alle Komponenten:

[htmforge-theme.css](../assets/css/htmforge-theme.css)

Einbinden über `Page.css_urls`:

```python
from htmforge.components.page import Page

class MyPage(Page):
    css_urls: list[str] = ["/static/htmforge-theme.css"]
```

Lade die Datei herunter und lege sie in deinen Static-Ordner (Flask: `static/`,
FastAPI: per `StaticFiles`-Mount, Django: `static/`).

## CSS-Klassen-Referenz

| Component | Klassen |
|---|---|
| Alert | `.alert`, `.alert-info/-success/-warning/-error`, `.alert-close` |
| Badge | `.badge`, `.badge-default/-primary/-success/...` |
| Breadcrumb | `nav > ol > li`, `[aria-current="page"]` |
| Modal | `.modal-wrapper`, `.modal-trigger`, `.modal`, `.modal-body`, `.modal-close` |
| DataTable | `.table-wrapper`, `.table` |
| Pagination | `.pagination`, `.active` |
| Spinner | `.spinner`, `.spinner-sm/-md/-lg` |
| Tabs | `.tabs`, `.tab`, `.tab-active` |
| Accordion | `.accordion`, `.accordion-item`, `.accordion-title`, `.accordion-content` |
| Dropdown | `.dropdown`, `.dropdown-trigger`, `.dropdown-menu`, `.dropdown-item` |
| Toast | `.toast`, `.toast-info/-success/-warning/-error` |
| Form | `.form` |
| RadioGroup | `.radiogroup`, `.radio-item` |
| FormField/SelectField/... | `.field-error`, `.field-wrapper`, `.checkbox-field`, `.form-group`, `.form-group-legend` |

(Vollständige Liste pro Component: jeweils im "Rendered HTML"-Block der
[Components Reference](../components/alert.md).)

## Eigene Klassen ergänzen

Jede Component erbt von `Component` das Feld `extra_cls`, mit dem sich eine
zusätzliche CSS-Klasse am Root-Element ergänzen lässt:

```python
Alert(message="Saved", extra_cls="my-extra-class")
```

`extra_cls` wird zusätzlich zur Default-Klasse gesetzt, nicht als Ersatz —
intern über `merge_cls()` (siehe `htmforge.core.element`), das leere/`None`-Werte
ignoriert und kein leeres `class=""` erzeugt. Bei Components mit mehreren
Klassen-Stellen (z.B. `Accordion`) prüfe im jeweiligen `render()`-Code, an
welches Element `extra_cls` konkret angehängt wird.

## Mit Tailwind/Bootstrap arbeiten

Verzichte auf das Default-Theme und setze deine Utility-Klassen direkt über `extra_cls`:

```python
Alert(message="Saved", extra_cls="rounded-lg bg-green-100 text-green-800 p-4")
```