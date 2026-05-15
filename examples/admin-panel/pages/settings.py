"""Settings page."""

from __future__ import annotations

from htmforge.components import Breadcrumb, Form, FormField, InputType, Toast, ToastVariant
from htmforge.core.element import Element
from htmforge.elements import button, div, h1, h2, p
from htmforge.htmx import HxSwap

from pages.base import BaseAdminPage


class SettingsPage(BaseAdminPage):
    """Settings page."""

    # Ensure the nav highlights the correct item
    active_nav: str = "Settings"

    def _body_content(self) -> list[Element | str | None]:
        """Render settings content."""
        content: list[Element | str | None] = [
            Breadcrumb(items=[("Home", "/"), ("Settings", None)]),
            h1("Settings"),
            div(
                Form(
                    action="/settings",
                    fields=[
                        FormField(
                            name="app_name",
                            label_text="Application Name",
                            input_type=InputType.TEXT,
                            value="htmforge Admin Panel",
                        ),
                        FormField(
                            name="admin_email",
                            label_text="Admin Email",
                            input_type=InputType.EMAIL,
                            value="admin@example.com",
                        ),
                    ],
                    hx_post="/settings",
                    hx_swap=HxSwap.NONE,
                    submit_label="Save Settings",
                ),
                cls="settings-card",
            ),
            div(
                h2("Danger Zone", cls="danger-title"),
                p("Reset all users to factory defaults. This cannot be undone."),
                button(
                    "Reset Demo Data",
                    cls="btn btn-danger",
                    hx_post="/settings/reset",
                    hx_target="#toast-slot",
                    hx_swap=HxSwap.OUTER_HTML,
                    hx_confirm="Reset all users? This cannot be undone.",
                ),
                div(id="toast-slot", cls="toast-slot"),
                cls="danger-zone",
            ),
        ]
        return self._render_admin_shell(content)
