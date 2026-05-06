# Quickstart — 5 minute walkthrough

1. Create a component with typed props.

```python
from htmforge import Component
from htmforge.elements import div, p


class Greeting(Component):
    name: str

    def render(self):
        return div(p(f"Hello {self.name}"))


print(Greeting(name="Ada").to_html())
```

Output:

```html
<div><p>Hello Ada</p></div>
```

2. Use element factories inside `render()`.

```python
from htmforge.elements import div, input, span


field = div(
    span("Name:"),
    input(type="search", name="q", cls="search"),
    cls="form-row",
)

print(field.to_html())
```

Output:

```html
<div class="form-row"><span>Name:</span><input type="search" name="q" class="search"></div>
```

3. Add HTMX attributes via typed enums or strings.

```python
from htmforge.elements import button
from htmforge.htmx import HxSwap


btn = button("Load", cls="primary", hx_get="/frag", hx_swap=HxSwap.INNER_HTML)
print(btn.to_html())
```

Output:

```html
<button class="primary" hx-get="/frag" hx-swap="innerHTML">Load</button>
```

4. Render to an HTML string with `to_html()`.

```python
from htmforge import Component
from htmforge.elements import div, p


class Greeting(Component):
    name: str

    def render(self):
        return div(p(f"Hello {self.name}"))


html = Greeting(name="Ada").to_html()
print(html)
```

Output:

```html
<div><p>Hello Ada</p></div>
```

5. Wire it into Flask.

```python
from flask import Flask

from htmforge import Component
from htmforge.elements import div, p


class Greeting(Component):
    name: str

    def render(self):
        return div(p(f"Hello {self.name}"))


app = Flask(__name__)


@app.route("/")
def index():
    return Greeting(name="Ada").to_flask()


if __name__ == "__main__":
    app.run(debug=True)
```
