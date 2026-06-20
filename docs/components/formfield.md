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
| `input_type` | `InputType` | `InputType.TEXT` | controls the `<input>` type — use `InputType.TEXTAREA` to render a `<textarea>` instead |
| `value` | `str` | `""` | current input value (used as the textarea content when `input_type` is `TEXTAREA`) |
| `placeholder` | `str` | `""` | placeholder text |
| `required` | `bool` | `False` | adds `required` and `aria-required` |
| `error` | `str` | `""` | renders an error block when set |
| `field_id` | `str` | `""` | overrides the generated id |
| `min` | `int \| float \| None` | `None` | sets the `min` attribute; only rendered for `InputType.NUMBER` |
| `max` | `int \| float \| None` | `None` | sets the `max` attribute; only rendered for `InputType.NUMBER` |

## Rendered HTML

```html
<div><label for="email">Email</label><input type="email" name="email" id="email"></div>
```

### Number field with bounds

```python
FormField(name="age", label_text="Age", input_type=InputType.NUMBER, min=18, max=120).to_html()
```

```html
<div><label for="age">Age</label><input type="number" name="age" id="age" min="18" max="120"></div>
```

### Textarea field

```python
FormField(name="bio", label_text="Bio", input_type=InputType.TEXTAREA).to_html()
```

```html
<div><label for="bio">Bio</label><textarea name="bio" id="bio"></textarea></div>
```

**Note:** `InputType.TEXTAREA` is the one input type that does not render an `<input>` element — the field's `value` becomes the `<textarea>`'s text content instead of a `value` attribute.