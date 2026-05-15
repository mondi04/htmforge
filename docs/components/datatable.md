# DataTable

DataTable renders a table with optional HTMX hooks for reloading rows.

```python
from htmforge.components import ColumnDef, DataTable

DataTable(
    columns=[ColumnDef(key="name", label="Name")],
    dict_rows=[{"name": "Ada"}],
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `headers` | `list[str]` | `[]` | Legacy header labels (use `columns` instead) |
| `rows` | `list[list[str]]` | `[]` | Legacy row data (use `dict_rows` instead) |
| `columns` | `list[ColumnDef] \| None` | `None` | Structured column definitions |
| `dict_rows` | `list[dict[str, str \| Element \| Component]] \| None` | `None` | Dict-based row data |
| `hx_url` | `str \| None` | `None` | Enables HTMX reload when set |
| `sort_url` | `str` | `""` | URL template for sortable headers |
| `current_sort` | `str` | `""` | Currently sorted column key |
| `sort_dir` | `str` | `"asc"` | Sort direction: "asc" or "desc" |
| `empty_message` | `str` | `"Keine Einträge"` | Shown when rows are empty |

## ColumnDef Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `key` | `str` | required | Dict key or column identifier |
| `label` | `str` | `""` | Display label (falls back to key) |
| `sortable` | `bool` | `False` | Renders as hx-get sort link |
| `width` | `str` | `""` | Optional CSS width |

## Usage

### Recommended: dict_rows + ColumnDef

```python
from htmforge.components import Badge, ColumnDef, DataTable

table = DataTable(
    columns=[
        ColumnDef(key="name", label="Name", sortable=True),
        ColumnDef(key="role", label="Role"),
    ],
    dict_rows=[
        {"name": "Ada", "role": Badge(text="Admin")},
        {"name": "Grace", "role": "Editor"},
    ],
    sort_url="/users/table",
    current_sort="name",
    sort_dir="asc",
)
```

### Legacy: headers + rows

```python
from htmforge.components import DataTable

legacy_table = DataTable(
    headers=["Name", "Email"],
    rows=[["Ada", "ada@example.com"], ["Grace", "grace@example.com"]],
)
```

## Rendered HTML

```html
<div class="table-wrapper"><table class="table"><thead><tr><th>Name</th></tr></thead><tbody><tr><td>Ada</td></tr></tbody></table></div>
```
