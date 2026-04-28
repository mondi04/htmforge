# Flask example

The `examples/flask_demo.py` file shows a minimal Flask app that renders a `UsersPage` using `Page` and an HTMX-powered `DataTable` + `Pagination` fragment endpoint.

Run:

```bash
pip install flask
python examples/flask_demo.py
# open http://127.0.0.1:5000/users
```

Key points:
- `UsersPage` is a `Page` subclass that returns `UsersPage(...).to_html()` for the full page
- `/users/table` returns only the table + pagination fragment for HTMX swaps
