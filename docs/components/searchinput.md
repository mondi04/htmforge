# SearchInput

Text input with automatic HTMX debounce (`keyup delay:...`).

Props

- `name` | `str` | required
- `search_url` | `str` | required — URL used for `hx-get`
- `search_target` | `str` | required — CSS selector for swap target
- `placeholder` | `str` | default `Suchen…`
- `debounce_ms` | `int` | default `300`
- `indicator` | `str` | default `""`

Usage

```python
from htmforge.components import SearchInput
s = SearchInput(name="q", search_url="/search", search_target="#results")
print(s.to_html())
```

Renders an `<input type="search">` with `hx-get`, `hx-trigger` and `hx-target` attributes.
