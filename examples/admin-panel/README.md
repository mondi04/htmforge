# htmforge Admin Panel Demo

A fully working user admin panel built with FastAPI + htmforge.
Demonstrates: DataTable, Modal, Form, SearchInput, Pagination, Toast, Badge, Spinner, Breadcrumb, Alert.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000

## What to look at

- `main.py`: all routes, kept short by delegating layout and forms
- `pages/base.py`: how `Page` is extended for a site-wide layout
- `pages/users.py`: composing htmforge components into a full page
- `components/user_form.py`: reusable form component with validation errors

## Screenshots

Placeholder for future screenshots. The demo is intentionally self-contained and should work immediately after installation.

## Code quality rules

- Type-annotate everything
- No hardcoded HTML strings for UI structure
- Keep `main.py` focused on route logic
- All HTMX attributes use htmforge enums or helpers where practical
- Comments on every route explain which htmforge feature it demonstrates