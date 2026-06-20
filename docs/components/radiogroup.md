# RadioGroup

Group of radio buttons with optional legend label and error injection support for form validation.

```python
from htmforge.components import RadioGroup

RadioGroup(
    name="plan",
    options=[("Basic", "basic"), ("Pro", "pro"), ("Enterprise", "enterprise")],
    selected="pro",
    legend_text="Select Plan",
    required=True
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `name` | `str` | required | Shared name attribute for all radios in the group |
| `options` | `list[tuple[str, str]]` | required | List of (label, value) tuples |
| `selected` | `str` | `""` | Currently selected option value |
| `legend_text` | `str` | `""` | Group legend text; omitted if empty |
| `required` | `bool` | `False` | Sets `required` on first radio only |
| `error` | `str` | `""` | Error message; renders as `div.field-error` if set |
| `extra_cls` | `str` | `""` | Extra CSS class appended to the `fieldset` (inherited from `Component`) |

## Rendered HTML

```html
<fieldset class="radiogroup"><legend>Select Plan</legend><div class="radio-item"><input type="radio" name="plan" id="plan-basic" value="basic"><label for="plan-basic">Basic</label></div><div class="radio-item"><input type="radio" name="plan" id="plan-pro" value="pro" checked required><label for="plan-pro">Pro</label></div><div class="radio-item"><input type="radio" name="plan" id="plan-enterprise" value="enterprise"><label for="plan-enterprise">Enterprise</label></div></fieldset>
```

**Note:** Rendered in a `<fieldset class="radiogroup">` with radio items in individual `div.radio-item` containers. The `required` attribute is only set on the first radio button. Use `extra_cls` to add custom styling classes.