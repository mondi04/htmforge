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
| `close_label` | `str` | `Close` | label for the close button |

## Rendered HTML

```html
<div class="modal-wrapper"><button type="button" data-modal-target="confirm" class="modal-trigger" hx-get="/modal/content" hx-target="#confirm-body" hx-swap="innerHTML">Open</button><dialog id="confirm" class="modal"><div id="confirm-body" class="modal-body"></div><form method="dialog"><button class="modal-close">Close</button></form></dialog><script>if(!window.__htmforgeModalDelegated){window.__htmforgeModalDelegated=true;document.addEventListener('click',function(e){var btn=e.target.closest('[data-modal-target]');if(!btn)return;var dlg=document.getElementById(btn.getAttribute('data-modal-target'));if(dlg&&!dlg.open)dlg.showModal();});}</script></div>
```

**Multiple modals on one page:** the delegated click listener is registered exactly once (guarded by `window.__htmforgeModalDelegated`), regardless of how many `Modal` instances render their own `<script>` tag. Each trigger click is matched via `closest('[data-modal-target]')` and `showModal()` is only called when the dialog isn't already open, so two or more modals on the same page never double-fire or throw `InvalidStateError` (see #16).
