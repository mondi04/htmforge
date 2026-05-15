"""FastAPI application for the htmforge admin panel demo."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form as FastAPIForm
from typing import cast, Literal
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from components.user_form import UserForm
from fake_db import create_user, delete_user, get_user, list_users, reset_users, update_user
from htmforge.components import Alert, AlertVariant, Breadcrumb, Toast, ToastVariant
from htmforge.elements import div, raw
from pages.home import HomePage
from pages.settings import SettingsPage
from pages.users import PAGE_SIZE, UsersPage, build_users_fragment

app = FastAPI(title="htmforge Admin Panel Demo")

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def _validate_user(name: str, email: str, role: str, *, exclude_user_id: int | None = None) -> dict[str, str]:
    errors: dict[str, str] = {}
    clean_name = name.strip()
    clean_email = email.strip()

    if not clean_name:
        errors["name"] = "Name is required."
    if not clean_email:
        errors["email"] = "Email is required."
    elif "@" not in clean_email or "." not in clean_email.split("@")[1]:
        errors["email"] = "Enter a valid email address."
    if role not in {"admin", "editor", "viewer"}:
        errors["role"] = "Choose a valid role."

    for user in list_users(q="", page=1, per_page=10_000)[0]:
        if user["email"].casefold() == clean_email.casefold() and user["id"] != exclude_user_id:
            errors.setdefault("email", "That email address is already in use.")
            break

    return errors


def _modal_body(*children: object) -> str:
    return div(*children, id="modal-body", cls="modal-body", hx_swap_oob="true").to_html()


def _success_payload(message: str) -> str:
    users, total = list_users(q="", page=1, per_page=PAGE_SIZE)
    fragment = build_users_fragment(users, total, 1, PAGE_SIZE, "", oob=True).to_html()
    toast = Toast(message=message, variant=ToastVariant.SUCCESS).to_html()
    close_modal = raw(
        "<script>document.getElementById('modal').close();"
        "document.getElementById('modal-body').innerHTML='';</script>"
    )
    return fragment + toast + close_modal


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def home() -> str:
    """Home dashboard page."""
    users, total = list_users(q="", page=1, per_page=9999)
    recent = sorted(users, key=lambda u: u["created_at"], reverse=True)[:5]
    return HomePage(title="Dashboard · htmforge Admin", recent_users=recent, total_users=total, active_nav="Dashboard").to_html()


@app.get("/users", response_class=HTMLResponse)
def users_page(q: str = "", page: int = 1) -> str:
    # Demonstrates the full Page shell with search, table, pagination, modal, and breadcrumb.
    users, total = list_users(q=q, page=page, per_page=PAGE_SIZE)
    return UsersPage(title="Users · htmforge Admin", users=users, total_users=total, page=page, per_page=PAGE_SIZE, q=q, active_nav="Users").to_html()


@app.get("/users/search", response_class=HTMLResponse)
def users_search(q: str = "", page: int = 1) -> str:
    # Demonstrates the HTMX live-search fragment that updates only the user table region.
    users, total = list_users(q=q, page=page, per_page=PAGE_SIZE)
    return build_users_fragment(users, total, page, PAGE_SIZE, q).to_html()


@app.get("/users/new", response_class=HTMLResponse)
def users_new() -> str:
    # Demonstrates loading a modal body with a create form over HTMX.
    return div(
        Breadcrumb(items=[("Users", "/users"), ("Add User", None)]),
        UserForm(submit_label="Create user").render(),
    ).to_html()


@app.post("/users", response_class=HTMLResponse)
def users_create(
    name: str = FastAPIForm(...),
    email: str = FastAPIForm(...),
    role: str = FastAPIForm("viewer"),
) -> str:
    # Demonstrates Form + HTMX OOB swap for success, with modal-body replacement on validation errors.
    errors = _validate_user(name, email, role)
    if errors:
        return _modal_body(
            Alert(message="Please fix the highlighted fields.", variant=AlertVariant.ERROR, dismissible=True),
            Breadcrumb(items=[("Users", "/users"), ("Add User", None)]),
            UserForm(
                name=name,
                email=email,
                role=cast(Literal['admin', 'editor', 'viewer'], role if role in {"admin", "editor", "viewer"} else "viewer"),
                errors=errors,
                submit_label="Create user",
            ).render(),
        )

    create_user(name=name, email=email, role=role)  # type: ignore[arg-type]
    return _success_payload(f"Created {name.strip()}.")


@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
def users_edit(user_id: int) -> str:
    # Demonstrates loading a pre-filled edit form into the modal body.
    user = get_user(user_id)
    if user is None:
        return Alert(message="User not found.", variant=AlertVariant.ERROR, dismissible=True).to_html()

    return div(
        Breadcrumb(items=[("Users", "/users"), ("Edit User", None)]),
        UserForm(
            user_id=user_id,
            name=user["name"],
            email=user["email"],
            role=cast(Literal['admin', 'editor', 'viewer'], user["role"]),
            use_put=True,
            submit_label="Save changes",
        ).render(),
    ).to_html()


@app.put("/users/{user_id}", response_class=HTMLResponse)
def users_update(
    user_id: int,
    name: str = FastAPIForm(...),
    email: str = FastAPIForm(...),
    role: str = FastAPIForm("viewer"),
) -> str:
    # Demonstrates PUT-based HTMX form submission with OOB table refresh and toast feedback.
    errors = _validate_user(name, email, role, exclude_user_id=user_id)
    if errors:
        return _modal_body(
            Alert(message="Please fix the highlighted fields.", variant=AlertVariant.ERROR, dismissible=True),
            Breadcrumb(items=[("Users", "/users"), ("Edit User", None)]),
            UserForm(
                user_id=user_id,
                name=name,
                email=email,
                role=cast(Literal['admin', 'editor', 'viewer'], role if role in {"admin", "editor", "viewer"} else "viewer"),
                errors=errors,
                use_put=True,
                submit_label="Save changes",
            ).render(),
        )

    updated = update_user(user_id, name=name, email=email, role=role)  # type: ignore[arg-type]
    return _success_payload(f"Updated {updated['name']}.")


@app.delete("/users/{user_id}", response_class=HTMLResponse)
def users_delete(user_id: int) -> Response:
    # Demonstrates row-level deletion with hx-delete and no extra HTML payload.
    delete_user(user_id)
    return Response(status_code=200)


@app.get("/settings", response_class=HTMLResponse)
def settings_page() -> str:
    """Settings page."""
    return SettingsPage(title="Settings · htmforge Admin", active_nav="Settings").to_html()


@app.post("/settings", response_class=HTMLResponse)
def save_settings() -> str:
    """Save settings (in-memory only)."""
    return Toast(message="Settings saved!", variant=ToastVariant.SUCCESS).to_html()


@app.post("/settings/reset", response_class=HTMLResponse)
def reset_data() -> str:
    """Reset demo data."""
    reset_users()
    return Toast(message="Demo data reset!", variant=ToastVariant.SUCCESS).to_html()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)