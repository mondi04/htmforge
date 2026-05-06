# Tabs

Tab navigation with HTMX lazy-loading support. Each tab fetches its content from a URL via HTMX.

```python
from htmforge.components import Tabs

Tabs(
    tabs=[("Overview", "/tabs/overview"), ("Details", "/tabs/details")],
    active=0,
    target="#tab-panel"
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `tabs` | `list[tuple[str, str]]` | required | List of (label, url) tuples for each tab |
| `active` | `int` | `0` | Index of the active tab (0-based) |
| `target` | `str` | `"#tab-panel"` | CSS selector for HTMX content swap |
| `tab_cls` | `str` | `""` | Extra CSS class on the tab bar wrapper |

## Rendered HTML

```html
<div class="tabs"><button class="tab tab-active" disabled>Overview</button><button class="tab" hx-get="/tabs/details" hx-target="#tab-panel" hx-swap="innerHTML">Details</button></div>
```

**Note:** The active tab is disabled with no HTMX attributes. Inactive tabs have `hx-get`, `hx-target`, and `hx-swap` attributes for content loading.
