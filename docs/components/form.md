# Form

Form container with HTMX support and automatic validation error injection to matching fields.

```python
from htmforge.components import Form, SelectField, CheckboxField
from htmforge.htmx import HxSwap

Form(
    action="/users/create",
    method="post",
    fields=[
        SelectField(name="role", options=[("Admin", "admin"), ("User", "user")]),
        CheckboxField(name="active", label_text="Active")
    ],
    submit_label="Create User",
    errors={"role": "Role is required"},
    hx_post="/users/create",
    hx_target="#form-result",
    hx_swap=HxSwap.OUTER_HTML
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `action` | `str` | required | Form action URL (form attribute) |
| `method` | `str` | `"post"` | HTTP method: "get" or "post" |
| `fields` | `list[Component]` | `[]` | List of form field components |
| `submit_label` | `str` | `"Absenden"` | Submit button text |
| `errors` | `dict[str, str]` | `{}` | Validation errors: `{field_name: message}` |
| `hx_post` | `str` | `""` | HTMX POST URL (overrides action for HTMX) |
| `hx_target` | `str` | `""` | HTMX target selector |
| `hx_swap` | `HxSwap \| None` | `None` | HTMX swap strategy |

## Rendered HTML

```html
<form action="/users/create" method="post" hx-post="/users/create" hx-target="#form-result" hx-swap="outerHTML"><div><label for="role">Role</label><select name="role" id="role"><option value="admin">Admin</option><option value="user">User</option></select><div class="field-error">Role is required</div></div><div class="checkbox-field"><input type="checkbox" name="active" id="active" value="1"><label for="active">Active</label></div><button type="submit">Create User</button></form>
```

**Auto-Error Injection:** The `Form` component matches field names in the `errors` dict against each field's `name` property. When a match is found, the field is cloned with the error message set, and the error is rendered as `div.field-error`.
