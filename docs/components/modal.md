# Modal

Trigger button + dialog overlay. Content is loaded via HTMX into the dialog body.

Props

- `modal_id` | `str` | required
- `trigger_label` | `str` | required
- `hx_url` | `str` | required — URL to load content from
- `hx_target` | `str` | optional; overrides default body target
- `close_label` | `str` | default `Schließen`

Usage

```python
from htmforge.components import Modal
Modal(modal_id="confirm", trigger_label="Open", hx_url="/modal/content").to_html()
```

Rendered HTML: button with `data-modal-target` and a `<dialog id=...>` plus inline script to call `showModal()` on click.
