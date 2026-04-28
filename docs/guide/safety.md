# XSS & Safety

`Element.to_html()` escapes all text children using `markupsafe.escape`.

- `_render_children` calls `escape()` on plain strings (see `htmforge.core.element`).
- Use `safe_html()` when the string already contains trusted HTML; it returns a `Markup` object and is not escaped again.
- Use `raw()` from `htmforge.elements` for inline `<script>` or `<style>` content to avoid escaping.

Example:

```python
from htmforge.elements import div
from htmforge.core.element import safe_html

raw_html = safe_html("<strong>fett</strong>")
print(div(raw_html).to_html())  # <div><strong>fett</strong></div>
```

Attribute escaping is handled in `_render_attrs` via `markupsafe.escape` before emitting attribute values.
