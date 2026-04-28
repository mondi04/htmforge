# Framework Adapters

FastAPI / Flask / Django examples for returning a full page or an HTMX fragment.

- `Component.to_fastapi()` returns a `fastapi.responses.HTMLResponse` (requires `fastapi`).
- `Component.to_flask()` returns a `flask.Response` (requires `flask`).
- `Component.to_django()` returns a `django.http.HttpResponse` (requires `django`).

See `examples/fastapi_demo.py` for a complete FastAPI app.

### HTMX fragment vs full page

- Full page: return `Page(...).to_html()` (includes DOCTYPE).
- Fragment: return `component.render().to_html()` or `component.to_html()` for arbitrary fragments.
