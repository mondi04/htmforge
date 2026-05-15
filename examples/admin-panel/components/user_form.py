"""Reusable user form for create and edit flows."""

from __future__ import annotations

from htmforge import Component
from htmforge.components import Form, FormField, InputType, SelectField
from htmforge.core.element import Element
from htmforge.elements import button, form as html_form
from htmforge.htmx import HxSwap

from fake_db import UserRole

ROLE_OPTIONS: tuple[tuple[str, UserRole], ...] = (
    ("Admin", "admin"),
    ("Editor", "editor"),
    ("Viewer", "viewer"),
)


class UserForm(Component):
    """Create or edit a user inside the modal."""

    user_id: int | None = None
    name: str = ""
    email: str = ""
    role: UserRole = "viewer"
    errors: dict[str, str] = {}
    submit_label: str = "Save user"
    use_put: bool = False

    def _name_field(self) -> FormField:
        return FormField(
            name="name",
            label_text="Name",
            input_type=InputType.TEXT,
            value=self.name,
            required=True,
            error=self.errors.get("name", ""),
        )

    def _email_field(self) -> FormField:
        return FormField(
            name="email",
            label_text="Email",
            input_type=InputType.EMAIL,
            value=self.email,
            required=True,
            error=self.errors.get("email", ""),
        )

    def _role_field(self) -> SelectField:
        return SelectField(
            name="role",
            label_text="Role",
            options=[(label, value) for label, value in ROLE_OPTIONS],
            selected=self.role,
            required=True,
            error=self.errors.get("role", ""),
        )

    def render(self) -> Element:
        if self.use_put and self.user_id is not None:
            return html_form(
                self._name_field().render(),
                self._email_field().render(),
                self._role_field().render(),
                button(self.submit_label, type="submit", cls="primary-btn"),
                hx_put=f"/users/{self.user_id}",
                hx_swap=HxSwap.NONE,
                hx_target="#user-table",
                cls="user-form",
            )

        return Form(
            action="/users",
            method="post",
            fields=[self._name_field(), self._email_field(), self._role_field()],
            submit_label=self.submit_label,
            hx_post="/users",
            hx_swap=HxSwap.NONE,
            hx_target="#user-table",
        ).render()