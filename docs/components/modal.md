# Modal

Trigger button + dialog overlay. Content is loaded via HTMX into the dialog body.

```python
from htmforge.components import Modal

Modal(
    modal_id="confirm",
    trigger_label="Open",
    hx_url="/modal/content",
    close_label="Close",
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `modal_id` | `str` | required | id for the `<dialog>` and body container |
| `trigger_label` | `str` | required | label on the trigger button |
| `hx_url` | `str` | required | URL loaded into the modal body |
| `hx_target` | `str` | `""` | overrides the default body target when set |
| `close_label` | `str` | `Schließen` | label for the close button |

## Rendered HTML

```html
<div class="modal-wrapper"><button type="button" data-modal-target="confirm" class="modal-trigger" hx-get="/modal/content" hx-target="#confirm-body" hx-swap="innerHTML">Open</button><dialog id="confirm" class="modal"><div id="confirm-body" class="modal-body"></div><form method="dialog"><button class="modal-close">Close</button></form></dialog><script>document.querySelectorAll('[data-modal-target]').forEach(function(btn){btn.addEventListener('click',function(){var id=btn.getAttribute('data-modal-target');var dlg=document.getElementById(id);if(dlg)dlg.showModal();});});</script></div>
```
