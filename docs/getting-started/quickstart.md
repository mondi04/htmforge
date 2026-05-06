# Quickstart - 5 minute walkthrough

## 1. Create a Component

```python
from htmforge import Component
from htmforge.elements import div, p


class Greeting(Component):
    name: str

    def render(self):
        return div(p(f"Hello {self.name}!"), cls="greeting")

print(Greeting(name="Ada").to_html())
# Output: <div class="greeting"><p>Hello Ada!</p></div>
```

## 2. Use Element factories

```python
from htmforge.elements import button, input
from htmforge.htmx import HxSwap

btn = button(
    "Load",
    hx_get="/content",
    hx_swap=HxSwap.INNER_HTML,
)

search = input(
    type="search",
    name="q",
    hx_get="/search",
    hx_trigger="keyup delay:300ms",
    placeholder="Search users...",
)
```

## 3. Use pre-built Components (v0.3.0)

```python
from htmforge.components import (
    Alert,
    AlertVariant,
    DataTable,
    ColumnDef,
    Form,
    SelectField,
    Toast,
    ToastVariant,
    Spinner,
    SpinnerSize,
)

# Alert
alert = Alert(
    variant=AlertVariant.SUCCESS,
    content="Data saved!",
    dismissible=True,
)

# DataTable with sortable headers
table = DataTable(
    columns=[
        ColumnDef(key="name", label="Name", sortable=True),
        ColumnDef(key="email", label="Email", sortable=False),
    ],
    dict_rows=[
        {"name": "Ada Lovelace", "email": "ada@example.com"},
        {"name": "Grace Hopper", "email": "grace@example.com"},
    ],
    sort_url="/users?sort={col}&dir={dir}",
)

# Form with auto-error injection
form = Form(
    action="/contact",
    method="post",
    fields=[
        SelectField(
            name="subject",
            options=[("bug", "Bug Report"), ("feature", "Feature Request")],
        ),
    ],
    errors={"subject": "Please select a subject"},
)

# Toast notification
toast = Toast(
    variant=ToastVariant.INFO,
    content="Page refreshed",
    duration_ms=3000,
)

# Loading spinner
spinner = Spinner(size=SpinnerSize.MD)
```

## 4. Render to HTML

```python
# Direct string
html = greeting.to_html()

# Framework adapters
flask_response = greeting.to_flask()
fastapi_response = greeting.to_fastapi()
django_response = greeting.to_django()
```

## 5. Next Steps

- See [Installation](installation.md) for setup
- Read [Concepts](concepts.md) for architecture details
- View [Components](../api/components.md) for full API reference
- Check [Framework examples](../examples/fastapi.md) for FastAPI, Flask, Django
