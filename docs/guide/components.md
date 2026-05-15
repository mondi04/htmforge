# Components Guide

Components in htmforge are regular Python classes based on `Component`.
You declare typed fields, then return one root `Element` from `render()`.

## Core Component API

- Implement `render() -> Element` and return the root element.
- `validate_assignment=True` ensures runtime prop changes are validated.
- Use `to_html()` to render a full HTML string.
- Use `to_fragment()` when you want an HTMX-friendly fragment.
- Use `clone(**overrides)` to create a modified copy.

`htmx_attrs()` returns only HTMX fields that are set. Dict values are serialized as compact JSON.

If a subclass does not implement `render()`, instantiation fails with `TypeError`.

## Minimal Example

```python
from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import div, h2, p


class UserCard(Component):
    name: str
    email: str

    def render(self) -> Element:
        return div(
            h2(self.name),
            p(self.email),
            cls="card",
        )


html = UserCard(name="Ada", email="ada@example.com").to_html()
```

## Framework Adapters

- `to_fastapi()` returns a FastAPI `HTMLResponse`
- `to_flask()` returns a Flask `Response`
- `to_django()` returns a Django `HttpResponse`

```python
page = UserCard(name="Ada", email="ada@example.com")
fastapi_response = page.to_fastapi()
```

## HTMX Integration

You can set typed HTMX values either on elements or components.

```python
from htmforge.elements import button
from htmforge.htmx import HxSwap, HxTarget

delete_btn = button(
    "Delete",
    hx_delete="/users/1",
    hx_swap=HxSwap.OUTER_HTML,
    hx_target=HxTarget.CLOSEST_TR,
    hx_confirm="Delete this user?",
)
```

## Pre-built Components

### Data and Feedback

- `DataTable` for tabular data with legacy and dict-row modes
- `Alert` for status messages
- `Badge` and `Breadcrumb` for small metadata and navigation hints
- `Pagination` for page controls
- `Toast` for timed notifications

### Interaction

- `Modal` for dialog flows
- `SearchInput` for debounced search
- `Tabs` for HTMX tab panels
- `Accordion` for expandable sections
- `Dropdown` for action menus
- `Spinner` for loading states

### Forms

- `FormField` for single field rendering
- `SelectField`, `CheckboxField`, `RadioGroup` for typed controls
- `FormGroup` for grouped layouts
- `Form` for full forms with automatic error injection

```python
from htmforge.components import Form, FormField, InputType

form = Form(
    action="/register",
    fields=[
        FormField(name="username", label_text="Username", input_type=InputType.TEXT),
        FormField(name="email", label_text="Email", input_type=InputType.EMAIL),
    ],
    errors={"email": "This email is already registered."},
    submit_label="Create account",
)
```
