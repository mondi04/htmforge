# DataTable

DataTable renders a table with optional HTMX hooks for reloading rows.

```python
from htmforge.components import DataTable

DataTable(headers=["Name"], rows=[["Ada"]]).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `headers` | `list[str]` | required | table header labels |
| `rows` | `list[list[str]]` | required | table body rows |
| `hx_url` | `str | None` | `None` | enables HTMX reload when set |
| `empty_message` | `str` | `Keine Einträge` | shown when `rows` is empty |

## Rendered HTML

```html
<div class="table-wrapper"><table class="table"><thead><tr><th>Name</th></tr></thead><tbody><tr><td>Ada</td></tr></tbody></table></div>
```
