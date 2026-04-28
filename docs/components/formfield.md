# FormField

Label + input + optional error block.

Props (from `htmforge.components.form_field`):
- `name` | `str` | required
- `label_text` | `str` | optional
- `input_type` | enum `InputType` | default `TEXT`
- `required` | `bool` | default `False`
- `error` | `str` | optional

Minimal example:

```python
from htmforge.components import FormField, InputType
FormField(name="email", label_text="Email", input_type=InputType.EMAIL).to_html()
```
