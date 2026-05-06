# Accordion

Multiple expandable sections using native HTML `details` and `summary` elements for semantic markup.

```python
from htmforge.components import Accordion

Accordion(
    items=[("FAQ", "Answer text"), ("Info", "More details")],
    open_index=0
).to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `items` | `list[tuple[str, str]]` | required | List of (title, content) tuples |
| `open_index` | `int \| None` | `None` | Index of initially open item; `None` = all closed |
| `item_cls` | `str` | `""` | Extra CSS class on each details element |

## Rendered HTML

```html
<div class="accordion"><details class="accordion-item" open><summary class="accordion-title">FAQ</summary><div class="accordion-content">Answer text</div></details><details class="accordion-item"><summary class="accordion-title">Info</summary><div class="accordion-content">More details</div></details></div>
```

**Note:** Uses semantic HTML `<details>` and `<summary>` elements. The `open` attribute controls initial state. Only one section opens at a time via browser default behavior.
