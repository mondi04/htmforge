# FastAPI example

See `examples/fastapi_demo.py` in the repository. This example shows a full page `UsersPage` implemented as a `Page` subclass, an in-memory data store, a `DataTable` with HTMX-powered pagination, and a POST handler that returns the updated page.

Key points:

- The page uses `DataTable` and `Pagination` wired to `/users/table` for HTMX fragments.
- The server returns either the full page (`/users`) or the fragment (`/users/table`).

Full file: `examples/fastapi_demo.py` (in repo)
