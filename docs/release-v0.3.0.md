# htmforge v0.3.0 Release Notes

**Release Date:** May 6, 2026  
**Version:** 0.3.0  
**Status:** Production Ready ✅

---

## What's New in v0.3.0?

v0.3.0 introduces **20+ new features** across 5 implementation blocks (F through J), including new components, enhanced data handling, a complete forms system, API extensions, and comprehensive testing infrastructure.

### Quick Stats
- **20+ Components** (5 new, 10 enhanced, 5 existing)
- **238 Tests** passing (+ 5 skipped optional Django)
- **100% Type Safe** — mypy strict clean
- **0 Breaking Changes** — Backward compatible with v0.2.x

---

## Block F: DataTable Enhancements

Structured column definitions and dict-based rendering.

### New Features
- `ColumnDef` class: Structured columns with key, label, sortable, width
- Dict rows: Render from `list[dict[str, str]]` — fully backward compatible
- Sortable headers: Click headers to sort via HTMX
- Sort tracking: `sort_url`, `current_sort`, `sort_dir` fields

### Example
```python
from htmforge.components import DataTable, ColumnDef

table = DataTable(
    columns=[
        ColumnDef(key="name", label="User", sortable=True),
        ColumnDef(key="email", label="Email Address", sortable=False),
    ],
    dict_rows=[
        {"name": "Ada Lovelace", "email": "ada@example.com"},
        {"name": "Grace Hopper", "email": "grace@example.com"},
    ],
    sort_url="/users?sort={col}&dir={dir}",
    current_sort="name",
    sort_dir="asc",
)
```

---

## Block G: New Components (5)

Five new interactive components for modern UI patterns.

### Spinner
Accessible loading indicator with size variants.

```python
from htmforge.components import Spinner, SpinnerSize

spinner = Spinner(size=SpinnerSize.LG)  # SM / MD / LG
```

### Tabs
Tab navigation with HTMX lazy-loading per inactive tab.

```python
from htmforge.components import Tabs

tabs = Tabs(
    tabs=[
        ("Dashboard", "/dashboard"),
        ("Settings", "/settings"),
        ("Profile", "/profile"),
    ],
    active=0,
)
```

### Toast
Timed notifications with HTMX OOB swap support.

```python
from htmforge.components import Toast, ToastVariant

toast = Toast(
    variant=ToastVariant.SUCCESS,
    content="Changes saved!",
    duration_ms=3000,
)
```

### Accordion
Collapsible sections using native `<details>/<summary>` elements.

```python
from htmforge.components import Accordion

accordion = Accordion(
    items=[
        ("Section 1", "Content 1"),
        ("Section 2", "Content 2"),
    ],
    open_index=0,
)
```

### Dropdown
Trigger button with menu items and optional HTMX toggle.

```python
from htmforge.components import Dropdown

dropdown = Dropdown(
    label="Actions",
    items=[
        ("Edit", "/edit"),
        ("Delete", "/delete", "/toggle/delete"),
    ],
)
```

**25 unit tests** ensure reliability and HTMX integration.

---

## Block H: Forms System (5 Components)

Complete form building with auto-error injection pattern.

### SelectField
Dropdown select with typed options.

```python
from htmforge.components import SelectField

field = SelectField(
    name="country",
    label_text="Country",
    options=[("us", "USA"), ("de", "Germany"), ("fr", "France")],
    required=True,
)
```

### CheckboxField
Single checkbox with inline label.

```python
from htmforge.components import CheckboxField

field = CheckboxField(
    name="agree",
    label_text="I agree to terms and conditions",
    value="yes",
)
```

### RadioGroup
Group of radio buttons with legend.

```python
from htmforge.components import RadioGroup

group = RadioGroup(
    name="role",
    legend_text="Select your role",
    options=[("admin", "Administrator"), ("user", "User"), ("guest", "Guest")],
)
```

### FormGroup
Container for multiple form fields with optional legend.

```python
from htmforge.components import FormGroup

group = FormGroup(
    legend_text="Personal Information",
    fields=[field1, field2, field3],
)
```

### Form
Main form wrapper with **auto-error injection** and HTMX support.

```python
from htmforge.components import (
    Form, SelectField, CheckboxField, FormGroup
)

form = Form(
    action="/contact",
    method="post",
    fields=[
        SelectField(name="subject", options=[...]),
        CheckboxField(name="subscribe", label_text="Subscribe"),
        FormGroup(legend_text="Address", fields=[...]),
    ],
    submit_label="Send Message",
    errors={
        "subject": "This field is required",
        "email": "Invalid email address",
    },  # Auto-binds to matching field names
    hx_post="/contact",  # Optional HTMX submit
    hx_target="#result",
    hx_swap="innerHTML",
)
```

**22 unit tests** cover form structure, error injection, and HTMX integration.

---

## Block I: API Extensions

New methods on `Element` and `Component` for advanced use cases.

### Element.__eq__ and __hash__
Compare elements by rendered HTML, enable deduplication.

```python
from htmforge.elements import div, p

el1 = div(p("Hello"))
el2 = div(p("Hello"))

assert el1 == el2  # Compare by rendered HTML
```

### Component.clone(**overrides)
Create new instance with changed properties.

```python
card1 = Card(title="Post 1", body="Content")
card2 = card1.clone(title="Post 2")  # Same body, different title
```

### Component.to_fragment()
Explicit HTMX fragment rendering method.

```python
fragment = component.to_fragment()  # No wrapper div
```

### htmforge.render()
Top-level convenience function for Element/Component rendering.

```python
from htmforge import render

html = render(my_component)
```

### htmforge.when()
Conditional rendering helper (returns Element or None).

```python
from htmforge import when
from htmforge.elements import div, p

content = div(
    when(user.is_admin, admin_panel),
    when(user.is_logged_in, user_menu),
    when(not user.is_logged_in, login_button),
)
```

---

## Block J: Testing Infrastructure

Comprehensive testing suite ensures quality and performance.

### Framework Adapters (14 tests)
- **FastAPI** (3 tests): `to_fastapi()` returns HTMLResponse
- **Flask** (6 tests): `to_flask()` returns Response with content-type
- **Django** (5 tests): Auto-skipped if not installed, `to_django()` returns HttpResponse
- Error handling for missing framework imports

### Snapshot Tests (21 tests)
Regression detection via auto-created HTML snapshots.

- Snapshots stored in `tests/snapshots/`
- Auto-created on first run
- Compared on subsequent runs
- Full coverage of all 20+ components

### Performance Benchmarks (5 tests)
All complete in <1-2 seconds for 1000 iterations.

- Element rendering: 1000x <1s
- Nested elements (ul/li): 1000x <1s
- DataTable (10 rows): 1000x <2s
- Alert component: 1000x <1s
- render() helper: 1000x <1s

---

## Quality Metrics

### Testing
- **238 tests passing** ✅
- **5 tests skipped** (Django optional)
- **100% success rate**

### Type Safety
- **mypy --strict**: All 22 source files clean
- **0 type errors**

### Code Quality
- **ruff lint**: All checks passed
- **ruff format**: All files formatted

### Backward Compatibility
- ✅ All v0.2.x APIs continue working
- ✅ No breaking changes
- ✅ Safe to upgrade

---

## Migration Guide (v0.2.1 → v0.3.0)

### No Action Required
Your existing v0.2.1 code works without changes:
- `DataTable` with `rows` parameter: Still works ✅
- `FormField`: Still works ✅
- All existing components: Still work ✅

### Recommended Upgrades

#### 1. Use new DataTable API
```python
# Old (still works)
table = DataTable(headers=["Name", "Email"], rows=[...])

# New (better)
table = DataTable(
    columns=[
        ColumnDef(key="name", label="Name", sortable=True),
        ColumnDef(key="email", label="Email"),
    ],
    dict_rows=[...]
)
```

#### 2. Use new Forms System
```python
# Old (still works)
field = FormField(name="email", input_type=InputType.EMAIL)

# New (recommended)
form = Form(
    fields=[
        SelectField(name="type", options=[...]),
        CheckboxField(name="agree", label_text="I agree"),
    ],
    errors=form_errors,
)
```

---

## Installation

Install or upgrade with pip:

```bash
pip install --upgrade htmforge
```

Verify the version:

```python
import htmforge
print(htmforge.__version__)  # 0.3.0
```

---

## Documentation

- **API Reference**: [htmforge.components](../api/components.md)
- **Component Guide**: [Components](../guide/components.md)
- **Getting Started**: [Quickstart](../getting-started/quickstart.md)
- **Examples**: [FastAPI](../examples/fastapi.md), [Flask](../examples/flask.md), [Django](../examples/django.md)

---

## Changelog

See [CHANGELOG](changelog.md) for complete list of changes, bug fixes, and deprecations.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/mondi04/htmforge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mondi04/htmforge/discussions)
- **Docs**: [mondi04.github.io/htmforge](https://mondi04.github.io/htmforge)

---

## Next Steps (v1.0.0)

- Stable API guarantee
- Full mkdocs API reference with examples
- Django example app
- 100% docstring coverage

**Thank you for using htmforge!** 🚀
