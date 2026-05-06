# Components Guide

Subclass htmforge.Component and declare typed props as Pydantic fields.

## Core Component API

- Implement ender() -> Element and return the root Element.
- alidate_assignment=True ensures runtime prop assignment is validated.
- Use 	o_html() to get the rendered HTML string.
- clone(**overrides) creates a new instance with changed properties.
- 	o_fragment() renders as HTMX fragment (no wrapper div).

htmx_attrs() returns only set HTMX props; dicts are compact JSON-serialized.

__init_subclass__ guard raises TypeError if ender is missing at instantiation.

## Framework Adapters

- 	o_fastapi() → FastAPI HTMLResponse
- 	o_flask() → Flask Response
- 	o_django() → Django HttpResponse

## HTMX Integration

Example button using htmx props:

`python
from htmforge.elements import button
from htmforge.htmx import HxSwap

btn = button("Delete", hx_delete="/users/1", hx_swap=HxSwap.OUTER_HTML)
`

## Pre-built Components (v0.3.0)

### Block F: DataTable
Use ColumnDef for structured columns with optional sort support:

`python
from htmforge.components import DataTable, ColumnDef

table = DataTable(
    columns=[
        ColumnDef(key="name", label="User Name", sortable=True),
        ColumnDef(key="email", label="Email", sortable=False),
    ],
    dict_rows=[
        {"name": "Ada Lovelace", "email": "ada@example.com"},
        {"name": "Grace Hopper", "email": "grace@example.com"},
    ],
    sort_url="/users?sort={col}&dir={dir}",
    current_sort="name",
    sort_dir="asc",
)
`

### Block G: Interactive Components
- Spinner(size=SpinnerSize.MD) — accessible loading indicator
- Tabs(tabs=[("Tab 1", "/content/1"), ("Tab 2", "/content/2")], active=0)
- Toast(variant=ToastVariant.SUCCESS, content="Saved!", duration_ms=3000)
- Accordion(items=["Section 1", "Section 2"], open_index=0)
- Dropdown(label="Menu", items=[("Link", "/link")])

### Block H: Forms System
Build complete forms with auto-error injection:

`python
from htmforge.components import Form, SelectField, CheckboxField, RadioGroup

form = Form(
    action="/submit",
    method="post",
    fields=[
        SelectField(name="country", options=[("us", "USA"), ("de", "Germany")]),
        CheckboxField(name="agree", label_text="I agree to terms"),
        RadioGroup(name="role", options=[("admin", "Admin"), ("user", "User")]),
    ],
    errors={"country": "Please select a country"}  # Auto-binds to SelectField
)
`

## Legacy (v0.2.x)

FormField provides label + input + error for simple forms. Use Block H Form for advanced forms with auto-error injection.
