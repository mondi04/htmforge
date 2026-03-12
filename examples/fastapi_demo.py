"""FastAPI demo — htmforge in action.

Run with:
    pip install fastapi uvicorn htmforge
    uvicorn examples.fastapi_demo:app --reload

Then open http://localhost:8000/users
"""

from __future__ import annotations

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from htmforge.components import Alert, AlertVariant, DataTable, FormField, InputType, Pagination
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import div, h1, h2

app = FastAPI(title="htmforge demo")

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

_USERS: list[list[str]] = [
    ["Ada Lovelace", "ada@example.com"],
    ["Grace Hopper", "grace@example.com"],
    ["Margaret Hamilton", "margaret@example.com"],
]

PAGE_SIZE = 2


# ---------------------------------------------------------------------------
# Page component
# ---------------------------------------------------------------------------


class UsersPage(Page):
    """Full HTML page that lists users with a form to add a new one."""

    users: list[list[str]]
    current_page: int = 1
    total_pages: int = 1
    success_message: str = ""

    def _body_content(self) -> list[Element | str | None]:
        # Optional success alert (rendered out-of-band by HTMX on POST)
        alert: Element | None = None
        if self.success_message:
            alert = Alert(
                message=self.success_message,
                variant=AlertVariant.SUCCESS,
                dismissible=True,
            ).render()

        table = DataTable(
            headers=["Name", "Email"],
            rows=self.users,
            hx_url=f"/users/table?page={{page}}",
        ).render()

        pager = Pagination(
            current_page=self.current_page,
            total_pages=self.total_pages,
            hx_url="/users/table?page={page}",
            hx_target="#users-table",
        ).render()

        # Add-user form
        name_field = FormField(
            name="name",
            label_text="Full Name",
            input_type=InputType.TEXT,
            required=True,
        ).render()
        email_field = FormField(
            name="email",
            label_text="Email",
            input_type=InputType.EMAIL,
            required=True,
        ).render()

        return [
            div(
                alert,
                h1("Users"),
                div(table, pager, id="users-table"),
                h2("Add User"),
                div(name_field, email_field),
            )
        ]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


def _paginate(page: int) -> tuple[list[list[str]], int]:
    """Return the current page slice and total page count."""
    total = max(1, -(-len(_USERS) // PAGE_SIZE))  # ceiling division
    start = (page - 1) * PAGE_SIZE
    return _USERS[start : start + PAGE_SIZE], total


@app.get("/users", response_class=HTMLResponse)
def list_users(page: int = 1) -> str:
    """Render the full users page."""
    rows, total = _paginate(page)
    return UsersPage(
        title="Users — htmforge demo",
        css_urls=["https://cdn.jsdelivr.net/npm/water.css@2/out/water.css"],
        js_urls=["https://unpkg.com/htmx.org@1.9.12"],
        users=rows,
        current_page=page,
        total_pages=total,
    ).to_html()


@app.get("/users/table", response_class=HTMLResponse)
def users_table_fragment(page: int = 1) -> str:
    """Return only the table + pagination fragment for HTMX swaps."""
    rows, total = _paginate(page)
    table = DataTable(headers=["Name", "Email"], rows=rows).render().to_html()
    pager = Pagination(
        current_page=page,
        total_pages=total,
        hx_url="/users/table?page={page}",
        hx_target="#users-table",
    ).render().to_html()
    return table + pager


@app.post("/users", response_class=HTMLResponse)
def add_user(name: str = Form(...), email: str = Form(...)) -> str:
    """Add a user and return the updated full page."""
    _USERS.append([name, email])
    rows, total = _paginate(1)
    return UsersPage(
        title="Users — htmforge demo",
        css_urls=["https://cdn.jsdelivr.net/npm/water.css@2/out/water.css"],
        js_urls=["https://unpkg.com/htmx.org@1.9.12"],
        users=rows,
        current_page=1,
        total_pages=total,
        success_message=f"User '{name}' added successfully.",
    ).to_html()
