# Components

Subclass `htmforge.Component` and declare typed props as Pydantic fields.

- Implement `render() -> Element` and return the root `Element`.
- `validate_assignment=True` ensures runtime prop assignment is validated.
- Use `to_html()` to get the rendered HTML string.

`htmx_attrs()` returns only set HTMX props; dicts are compact JSON-serialized.

`__init_subclass__` guard raises `TypeError` if `render` is missing at instantiation.

Example button using htmx props:

```python
from htmforge.elements import button
from htmforge.htmx import HxSwap

btn = button("Delete", hx_delete="/users/1", hx_swap=HxSwap.OUTER_HTML)
```
