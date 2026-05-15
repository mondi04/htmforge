"""Users page and reusable table fragments."""

from __future__ import annotations

from math import ceil
from urllib.parse import quote_plus

from htmforge.components import (
    Alert,
    AlertVariant,
    Badge,
    BadgeVariant,
    Breadcrumb,
    ColumnDef,
    DataTable,
    Modal,
    Pagination,
    SearchInput,
    Spinner,
    SpinnerSize,
)
from htmforge.core.element import Element
from htmforge.elements import button, div, h1, p, section
from htmforge.htmx import HxSwap, HxTarget

from fake_db import User, UserRole
from pages.base import BaseAdminPage

PAGE_SIZE = 5
ROLE_BADGES: dict[UserRole, BadgeVariant] = {
    "admin": BadgeVariant.DANGER,
    "editor": BadgeVariant.WARNING,
    "viewer": BadgeVariant.SUCCESS,
}


def _role_badge(role: UserRole) -> Badge:
    return Badge(text=role.title(), variant=ROLE_BADGES[role])


def _action_buttons(user_id: int) -> Element:
    return div(
        button(
            "Edit",
            type="button",
            cls="action-btn action-btn-secondary",
            hx_get=f"/users/{user_id}/edit",
            hx_target="#modal-body",
            hx_swap=HxSwap.INNER_HTML,
            onclick="document.getElementById('modal').showModal()",
        ),
        button(
            "Delete",
            type="button",
            cls="action-btn action-btn-danger",
            hx_delete=f"/users/{user_id}",
            hx_target=HxTarget.CLOSEST_TR,
            hx_swap=HxSwap.OUTER_HTML,
            hx_confirm="Delete this user?",
        ),
        cls="row-actions",
    )


def _row(user: User) -> dict[str, str | Element | Badge]:
    return {
        "name": user["name"],
        "email": user["email"],
        "role": user["role"].capitalize(),
        "created_at": user["created_at"],
        "actions": "Edit · Delete",
    }


def build_users_fragment(
    users: list[User],
    total_users: int,
    page: int,
    per_page: int = PAGE_SIZE,
    q: str = "",
    *,
    oob: bool = False,
) -> Element:
    """Build the users table + pagination fragment."""

    total_pages = max(1, ceil(total_users / per_page))
    encoded_query = quote_plus(q.strip())
    container_attrs: dict[str, object] = {"id": "user-table", "cls": "table-panel"}
    if oob:
        container_attrs["hx_swap_oob"] = "true"

    return div(
        DataTable(
            columns=[
                ColumnDef(key="name", label="Name"),
                ColumnDef(key="email", label="Email"),
                ColumnDef(key="role", label="Role"),
                ColumnDef(key="created_at", label="Created"),
                ColumnDef(key="actions", label="Actions"),
            ],
            dict_rows=[_row(user) for user in users],
            empty_message="No users match your search.",
        ),
        Pagination(
            current_page=page,
            total_pages=total_pages,
            hx_url=f"/users/search?q={encoded_query}&page={{page}}",
            hx_target="#user-table",
        ),
        **container_attrs,
    )


def _toolbar() -> Element:
    return div(
        div(
            SearchInput(
                name="q",
                search_url="/users/search",
                search_target="#user-table",
                placeholder="Search users...",
                indicator="#search-spinner",
            ),
            div(
                Spinner(size=SpinnerSize.SM, label="Searching"),
                id="search-spinner",
                cls="htmx-indicator search-spinner",
            ),
            cls="search-shell",
        ),
        Modal(
            modal_id="modal",
            trigger_label="Add user",
            hx_url="/users/new",
            hx_target="#modal-body",
            close_label="Close",
        ),
        cls="admin-toolbar",
    )


class UsersPage(BaseAdminPage):
    """Full users page with search, table, modal trigger, and breadcrumbs."""

    # Ensure the nav highlights the correct item
    active_nav: str = "Users"

    users: list[User]
    total_users: int
    page: int
    per_page: int = PAGE_SIZE
    q: str = ""
    flash_message: str = ""
    flash_variant: AlertVariant = AlertVariant.SUCCESS

    def _content(self) -> list[Element | str | None]:
        items: list[Element | str | None] = [
            Breadcrumb(items=[("Home", "/"), ("Users", None)]),
            section(
                h1("Users", cls="page-title"),
                p(
                    f"{self.total_users} records total · page {self.page}",
                    cls="page-summary",
                ),
                cls="page-header",
            ),
            _toolbar(),
        ]

        if self.flash_message:
            items.append(
                Alert(
                    message=self.flash_message,
                    variant=self.flash_variant,
                    dismissible=True,
                )
            )

        items.extend(
            [
                build_users_fragment(self.users, self.total_users, self.page, self.per_page, self.q),
                div(id="toast", cls="toast-slot"),
            ]
        )
        return items