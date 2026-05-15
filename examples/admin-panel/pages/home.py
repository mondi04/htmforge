"""Home dashboard page."""

from __future__ import annotations

from htmforge import Component
from htmforge.components import Breadcrumb, ColumnDef, DataTable, Modal
from htmforge.core.element import Element
from htmforge.elements import a, div, h1, h2, p
from htmforge.htmx import HxSwap

from fake_db import User
from pages.base import BaseAdminPage
from pages.users import _role_badge


class StatCard(Component):
    """Stat card component showing a metric."""

    label: str
    count: int

    def render(self) -> Element:
        """Render a stat card."""
        return div(
            div(str(self.count), cls="stat-number"),
            div(self.label, cls="stat-label"),
            cls="stat-card",
        )


def build_recent_users_table(users: list[User]) -> Element:
    """Build table showing recent users."""
    return DataTable(
        columns=[
            ColumnDef(key="name", label="Name"),
            ColumnDef(key="email", label="Email"),
            ColumnDef(key="role", label="Role"),
        ],
        dict_rows=[
            {
                "name": user["name"],
                "email": user["email"],
                "role": user["role"].capitalize(),
            }
            for user in users
        ],
        empty_message="No recent users.",
    )


class HomePage(BaseAdminPage):
    """Home dashboard page."""

    # Ensure the nav highlights the correct item
    active_nav: str = "Dashboard"

    recent_users: list[User]
    total_users: int

    def _body_content(self) -> list[Element | str | None]:
        """Render dashboard content."""
        # Count users by role
        admin_count = sum(1 for u in self.recent_users if u["role"] == "admin")
        editor_count = sum(1 for u in self.recent_users if u["role"] == "editor")
        viewer_count = sum(1 for u in self.recent_users if u["role"] == "viewer")

        content: list[Element | str | None] = [
            Breadcrumb(items=[("Home", None)]),
            div(
                h1("Dashboard"),
                p("Welcome to the htmforge admin panel."),
                cls="page-header",
            ),
            div(
                StatCard(label="Total Users", count=self.total_users),
                StatCard(label="Admins", count=admin_count),
                StatCard(label="Editors", count=editor_count),
                StatCard(label="Viewers", count=viewer_count),
                cls="stats-grid",
            ),
            div(
                h2("Recent Users"),
                build_recent_users_table(self.recent_users),
                cls="section",
            ),
            div(
                h2("Quick Actions"),
                a(
                    "Manage Users",
                    href="/users",
                    cls="btn btn-primary",
                ),
                a(
                    "Add User",
                    href="#",
                    cls="btn btn-secondary",
                    hx_get="/users/new",
                    hx_target="#modal-body",
                    hx_swap=HxSwap.INNER_HTML,
                    onclick="document.getElementById('modal').showModal()",
                ),
                cls="quick-actions",
            ),
            Modal(
                modal_id="modal",
                trigger_label="Add user",
                hx_url="/users/new",
                hx_target="#modal-body",
                close_label="Close",
            ),
        ]
        return self._render_admin_shell(content)
