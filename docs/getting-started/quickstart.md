# Quickstart — 5 minute walkthrough

1. Create a Component with typed props

```python
from htmforge import Component
from htmforge.elements import div, p

class Greeting(Component):
    name: str
    def render(self):
        return div(p(f"Hello {self.name}"))

print(Greeting(name="Ada").to_html())
```

2. Use element factories inside `render()` (see above)

3. Add HTMX attributes via typed enums or strings

```python
from htmforge.elements import button
from htmforge.htmx import HxSwap

btn = button("Load", hx_get="/frag", hx_swap=HxSwap.INNER_HTML)
```

4. Render to HTML string: `component.to_html()`

5. Wire into Flask (example in docs/examples/flask.md)
