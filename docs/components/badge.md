# Badge

Small inline label with variant classes.

```python
from htmforge.components import Badge, BadgeVariant

Badge(text="New", variant=BadgeVariant.SUCCESS).to_html()
```

Props

- `text` | `str` | required
- `variant` | `BadgeVariant` | default `BadgeVariant.DEFAULT`

Rendered HTML:

```html
<span class="badge badge-success">New</span>
```
