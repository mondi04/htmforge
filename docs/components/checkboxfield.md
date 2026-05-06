# CheckboxField

Single checkbox input with label, validation support, and error injection for forms.

```python
from htmforge.components import CheckboxField

CheckboxField(
    name="newsletter",
    label_text="Subscribe to newsletter",
    checked=True,
    required=False
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `name` | `str` | required | name attribute of the input |
| `label_text` | `str` | required | Label text displayed next to checkbox |
| `checked` | `bool` | `False` | Pre-checked state |
| `value` | `str` | `"1"` | value attribute sent on form submission |
| `required` | `bool` | `False` | Sets `required` attribute on input |
| `error` | `str` | `""` | Error message; renders as `div.field-error` if set |
| `field_id` | `str` | `""` | HTML id attribute (defaults to `name` if empty) |

## Rendered HTML

```html
<div class="checkbox-field"><input type="checkbox" name="newsletter" id="newsletter" value="1" checked><label for="newsletter">Subscribe to newsletter</label></div>
```

**Note:** Used within `Form` components for automatic error injection based on field name matching. Label is always required and displayed to the right of the checkbox.
