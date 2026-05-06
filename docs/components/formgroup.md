# FormGroup

Layout container for grouping multiple form field components with optional legend label and custom CSS.

```python
from htmforge.components import FormGroup, SelectField, CheckboxField

FormGroup(
    fields=[
        SelectField(name="role", options=[("Admin", "admin"), ("User", "user")]),
        CheckboxField(name="active", label_text="Active User")
    ],
    legend_text="User Settings"
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `fields` | `list[Component]` | required | List of form field components to render |
| `legend_text` | `str` | `""` | Group legend text; renders as `div.form-group-legend` if set |
| `group_cls` | `str` | `""` | Extra CSS class on the wrapper div |

## Rendered HTML

```html
<div class="form-group"><div class="form-group-legend">User Settings</div><div><label for="role">Role</label><select name="role" id="role"><option value="admin">Admin</option><option value="user">User</option></select></div><div class="checkbox-field"><input type="checkbox" name="active" id="active" value="1"><label for="active">Active User</label></div></div>
```

**Note:** `FormGroup` is primarily a layout container. It renders all child fields by calling their `render()` methods. Use within `Form` for sectioning complex forms.
