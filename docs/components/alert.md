# Alert

Renders an alert box with an optional dismiss button.

```python
from htmforge.components import Alert, AlertVariant

Alert(message="Saved", variant=AlertVariant.SUCCESS, dismissible=True, close_label="Close").to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `message` | `str` | required | the alert text |
| `variant` | `AlertVariant` | `AlertVariant.INFO` | CSS variant |
| `dismissible` | `bool` | `False` | adds the close button |
| `close_label` | `str` | `Close` | `aria-label` for the close button |

## Rendered HTML

```html
<div class="alert alert-success">Saved<button type="button" class="alert-close" aria-label="Close" onclick="this.closest(&#39;.alert&#39;).remove()">×</button></div>
```
