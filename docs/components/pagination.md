# Pagination

Pagination shows previous/next and page numbers. Supports HTMX via `hx_url` and `hx_target` props.

```python
from htmforge.components import Pagination

Pagination(current_page=2, total_pages=3, hx_url="/p/{page}", hx_target="#list").to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `current_page` | `int` | required | current page number |
| `total_pages` | `int` | required | total number of pages |
| `hx_url` | `str` | required | URL template with `{page}` placeholder |
| `hx_target` | `str` | `""` | optional HTMX target selector |

## Rendered HTML

```html
<ul class="pagination"><li><a href="#" hx-get="/p/1" hx-target="#list">Previous</a></li><li><a href="#" hx-get="/p/1" hx-target="#list">1</a></li><li class="active"><a href="#">2</a></li><li><a href="#" hx-get="/p/3" hx-target="#list">3</a></li><li><a href="#" hx-get="/p/3" hx-target="#list">Next</a></li></ul>
```
