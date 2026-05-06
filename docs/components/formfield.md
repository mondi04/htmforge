# FormField

Label + input + optional error block.

```python
from htmforge.components import FormField, InputType

FormField(name="email", label_text="Email", input_type=InputType.EMAIL).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `name` | `str` | required | input name attribute |
| `label_text` | `str` | required | text rendered in the label |
| `input_type` | `InputType` | `InputType.TEXT` | controls the `<input>` type |
| `value` | `str` | `""` | current input value |
| `placeholder` | `str` | `""` | placeholder text |
| `required` | `bool` | `False` | adds `required` and `aria-required` |
| `error` | `str` | `""` | renders an error block when set |
| `field_id` | `str` | `""` | overrides the generated id |

## Rendered HTML

```html
<div><label for="email">Email</label><input type="email" name="email" id="email"></div>
```
