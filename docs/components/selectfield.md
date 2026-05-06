# SelectField

Dropdown select field with optional label, validation support, and error injection for form submission.

```python
from htmforge.components import SelectField

SelectField(
    name="role",
    options=[("Admin", "admin"), ("User", "user")],
    selected="user",
    label_text="Role",
    required=True
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `name` | `str` | required | name attribute of the select element |
| `options` | `list[tuple[str, str]]` | required | List of (label, value) tuples |
| `selected` | `str` | `""` | Currently selected option value |
| `label_text` | `str` | `""` | Field label text; omitted if empty |
| `required` | `bool` | `False` | Sets `required` attribute on select |
| `error` | `str` | `""` | Error message; renders as `div.field-error` if set |
| `field_id` | `str` | `""` | HTML id attribute (defaults to `name` if empty) |

## Rendered HTML

```html
<div><label for="role">Role</label><select name="role" id="role" required><option value="admin">Admin</option><option value="user" selected>User</option></select></div>
```

**Note:** Used within `Form` components for automatic error injection based on field name matching.
