# DataTable

DataTable renders a table with optional HTMX hooks for reloading rows.

Usage example is shown in `examples/fastapi_demo.py`.

Props (derived from source):
- `headers` | list[str] | required
- `rows` | list[list[str]] | required
- `empty_message` | str | default shown when no rows
- `hx_url` | str | optional — if provided, enables HTMX reloads

Edge cases: empty rows render a message row with colspan of the header count.
