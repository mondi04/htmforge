# Dropdown

Trigger button with hidden menu and optional HTMX toggle support for dynamic menu reloading.

```python
from htmforge.components import Dropdown

Dropdown(
    label="Actions",
    items=[("Edit", "/edit"), ("Delete", "/delete")],
    dropdown_id="actions-menu",
    toggle_url="/menu/toggle"
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `label` | `str` | required | Trigger button label |
| `items` | `list[tuple[str, str]]` | required | List of (label, url) tuples for menu items |
| `dropdown_id` | `str` | `"dropdown"` | Unique HTML id prefix (menu id becomes `{dropdown_id}-menu`) |
| `toggle_url` | `str` | `""` | HTMX URL to reload menu; if empty, no HTMX attributes added |

## Rendered HTML

```html
<div class="dropdown"><button class="dropdown-trigger" hx-get="/menu/toggle" hx-target="#actions-menu-menu" hx-swap="outerHTML">Actions</button><div id="actions-menu-menu" class="dropdown-menu"><a href="/edit" class="dropdown-item">Edit</a><a href="/delete" class="dropdown-item">Delete</a></div></div>
```

**Note:** When `toggle_url` is set, the button gets `hx-get`, `hx-target`, and `hx-swap` attributes. Use CSS to show/hide the menu div.
