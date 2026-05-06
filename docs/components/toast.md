# Toast

Timed notification box with HTMX out-of-band swap support for injecting notifications into existing pages.

```python
from htmforge.components import Toast, ToastVariant

Toast(
    message="Successfully saved!",
    variant=ToastVariant.SUCCESS,
    duration_ms=3000
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `message` | `str` | required | Notification text content |
| `variant` | `ToastVariant` | `ToastVariant.INFO` | Style: INFO, SUCCESS, WARNING, or ERROR |
| `toast_id` | `str` | `"toast"` | HTML id attribute; use OOB to inject into page |
| `duration_ms` | `int` | `3000` | Auto-dismiss delay in milliseconds (0 = no auto-dismiss) |

## Rendered HTML

```html
<div id="toast" class="toast toast-success" hx-swap-oob="true" data-duration="3000">Successfully saved!</div>
```

**Note:** Set `hx-swap-oob="true"` in HTMX responses to inject the toast out-of-band and replace an existing toast element. Variants: `toast-info`, `toast-success`, `toast-warning`, `toast-error`.
