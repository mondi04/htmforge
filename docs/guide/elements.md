# Elements

Attribute conversion rules (derived from `htmforge.core.element`):

- `cls` → `class`
- `for_` → `for`
- Leading/trailing underscores are stripped
- Underscores inside names become hyphens (`hx_get` → `hx-get`)
- `True` renders as flag-only attribute, `False`/`None` omitted

Void elements (from `_VOID_ELEMENTS`):

area, base, br, col, embed, hr, img, input, link, meta, param, source, track, wbr

`safe_html()` and `raw()`

- Use `safe_html(text)` when the string already contains trusted HTML — it returns a `Markup` instance.
- Use `raw()` (in `htmforge.elements`) when embedding inline `<script>`/`<style>` content to avoid escaping.

Factory list (grouped):

- Text: `p`, `span`, `strong`, `em`, `code`, `pre`, `blockquote`, `small`, `sub`, `sup`, `mark`, `kbd`, `abbr`, `time`
- Structure: `div`, `section`, `article`, `main`, `header`, `footer`, `nav`, `aside`
- Lists: `ul`, `ol`, `li`
- Tables: `table`, `thead`, `tbody`, `tfoot`, `tr`, `th`, `td`, `caption`, `colgroup`, `col`
- Forms: `form`, `input`, `label`, `button`, `select`, `option`, `textarea`, `fieldset`, `legend`
- Media: `img`, `picture`, `source`, `audio`, `video`, `track`, `figure`, `figcaption`, `canvas`, `iframe`
- Document: `html`, `head`, `body`, `title`, `meta`, `link`, `script`, `style`, `noscript`
- Interactive/Semantic: `dialog`, `details`, `summary`, `map_`, `area`

See `htmforge.elements` for the full canonical factory list.
