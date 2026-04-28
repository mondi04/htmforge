# HTMX Integration

Enums available (see `htmforge.htmx`):

- `HxSwap` — `innerHTML`, `outerHTML`, `beforebegin`, `afterbegin`, `beforeend`, `afterend`, `delete`, `none`
- `HxTrigger` — `click`, `change`, `keyup`, `load`, `revealed`, `intersect`, `every 1s`, `every 2s`
- `HxTarget` — `this`, `closest tr`, `closest div`, `next`, `previous`
- `HxPushUrl` — `true`, `false`

Use `hx_keyup_delay(ms)` helper to generate `keyup delay:{ms}ms` triggers.

Dict serialization example:

```python
component = MyComponent(hx_vals={"id": 1})
# renders hx-vals='{"id":1}'
```

Example: delete button with confirm + swap + target

```python
from htmforge.elements import button
from htmforge.htmx import HxSwap

btn = button(
    "Delete",
    hx_delete="/items/1",
    hx_confirm="Are you sure?",
    hx_swap=HxSwap.OUTER_HTML,
    hx_target="closest tr",
)
```
