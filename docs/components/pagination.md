# Pagination

Pagination shows previous/next and page numbers. Supports HTMX via `hx_url` and `hx_target` props.

Props (from source):
- `current_page` | int
- `total_pages` | int
- `hx_url` | str | optional
- `hx_target` | str | optional

Edge cases: when `total_pages <= 1` minimal markup is produced.
