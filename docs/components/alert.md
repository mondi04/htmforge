# Alert

Renders an alert box with optional dismiss button.

```python
from htmforge.components import Alert, AlertVariant

Alert(message="Saved", variant=AlertVariant.SUCCESS).to_html()
```

Props

- `message` | `str` | required — the alert text
- `variant` | `AlertVariant` | default `AlertVariant.INFO`
- `dismissible` | `bool` | default `False`
- `close_label` | `str` | default `Schließen`

Usage

```python
Alert(message="Saved", variant=AlertVariant.SUCCESS, dismissible=True).to_html()
```

Rendered HTML (example):

```html
<div class="alert alert-success">Saved<button type="button" class="alert-close" aria-label="Schließen">×</button></div>
```

HTMX: none specific.

Edge cases: when `dismissible=False` no close button is rendered.
