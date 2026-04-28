# Breadcrumb

Ordered nav list. Items are `(label, url)` tuples; use `url=None` for current item.

```python
from htmforge.components import Breadcrumb

Breadcrumb(items=[("Home","/"),("Products","/prod"),("Now",None)]).to_html()
```

Props

- `items` | `list[tuple[str, str | None]]` | required

Rendered HTML: contains `<nav><ol><li>...` with `aria-current="page"` for the current item.
