"""Snapshot-Tests: rendered HTML gegen gespeicherte Snapshots.

Snapshots werden beim ersten Run automatisch erstellt in
tests/snapshots/. Danach schlagen Tests fehl wenn sich
das HTML aendert - das ist gewollt (Regression-Detection).

Keine externe Abhaengigkeit - Snapshots werden als .html
Dateien gespeichert und mit pathlib gelesen/verglichen.
"""

from __future__ import annotations

import pathlib

from htmforge.components import (
    Accordion,
    Alert,
    AlertVariant,
    Badge,
    BadgeVariant,
    Breadcrumb,
    DataTable,
    Dropdown,
    Form,
    FormField,
    InputType,
    Modal,
    Pagination,
    SearchInput,
)
from htmforge.components.forms import CheckboxField, RadioGroup, SelectField
from htmforge.components.spinner import Spinner
from htmforge.components.tabs import Tabs
from htmforge.components.toast import Toast, ToastVariant

SNAPSHOT_DIR = pathlib.Path(__file__).parent / "snapshots"


def get_or_create_snapshot(name: str, html: str) -> str:
    """Liest Snapshot oder erstellt ihn beim ersten Run.

    Args:
        name: Dateiname ohne Extension (z.B. "alert_info")
        html: Das aktuelle gerenderte HTML

    Returns:
        Das gespeicherte Snapshot-HTML
    """
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    path = SNAPSHOT_DIR / f"{name}.html"
    if not path.exists():
        path.write_text(html, encoding="utf-8")
        return html
    return path.read_text(encoding="utf-8")


def assert_snapshot(name: str, html: str) -> None:
    """Vergleicht html mit gespeichertem Snapshot."""
    snapshot = get_or_create_snapshot(name, html)
    assert html == snapshot, (
        f"Snapshot mismatch for '{name}'.\n"
        f"Delete tests/snapshots/{name}.html to update."
    )


class TestComponentSnapshots:
    """Snapshot-Tests fuer alle fertigen Komponenten."""

    def test_alert_info_snapshot(self) -> None:
        html = Alert(message="Test").to_html()
        assert_snapshot("alert_info", html)

    def test_alert_success_dismissible_snapshot(self) -> None:
        html = Alert(
            message="Saved", variant=AlertVariant.SUCCESS, dismissible=True
        ).to_html()
        assert_snapshot("alert_success_dismissible", html)

    def test_badge_default_snapshot(self) -> None:
        html = Badge(text="New").to_html()
        assert_snapshot("badge_default", html)

    def test_badge_danger_snapshot(self) -> None:
        html = Badge(text="!", variant=BadgeVariant.DANGER).to_html()
        assert_snapshot("badge_danger", html)

    def test_breadcrumb_snapshot(self) -> None:
        html = Breadcrumb(
            items=[("Home", "/"), ("Products", "/prod"), ("Now", None)]
        ).to_html()
        assert_snapshot("breadcrumb", html)

    def test_datatable_snapshot(self) -> None:
        html = DataTable(
            headers=["Name", "Email"],
            rows=[["Ada", "ada@example.com"]],
        ).to_html()
        assert_snapshot("datatable", html)

    def test_datatable_empty_snapshot(self) -> None:
        html = DataTable(headers=["Name"], rows=[]).to_html()
        assert_snapshot("datatable_empty", html)

    def test_formfield_text_snapshot(self) -> None:
        html = FormField(name="username", label_text="Username").to_html()
        assert_snapshot("formfield_text", html)

    def test_formfield_email_required_snapshot(self) -> None:
        html = FormField(
            name="email",
            label_text="Email",
            input_type=InputType.EMAIL,
            required=True,
        ).to_html()
        assert_snapshot("formfield_email_required", html)

    def test_modal_snapshot(self) -> None:
        html = Modal(
            modal_id="confirm",
            trigger_label="Open",
            hx_url="/modal/content",
        ).to_html()
        assert_snapshot("modal", html)

    def test_pagination_snapshot(self) -> None:
        html = Pagination(
            current_page=2,
            total_pages=5,
            hx_url="/items?page={page}",
            hx_target="#list",
        ).to_html()
        assert_snapshot("pagination", html)

    def test_search_input_snapshot(self) -> None:
        html = SearchInput(
            name="q",
            search_url="/search",
            search_target="#results",
        ).to_html()
        assert_snapshot("search_input", html)

    def test_spinner_md_snapshot(self) -> None:
        html = Spinner().to_html()
        assert_snapshot("spinner_md", html)

    def test_tabs_snapshot(self) -> None:
        html = Tabs(
            tabs=[("Overview", "/overview"), ("Details", "/details")],
            active=0,
            target="#panel",
        ).to_html()
        assert_snapshot("tabs", html)

    def test_toast_success_snapshot(self) -> None:
        html = Toast(message="Saved", variant=ToastVariant.SUCCESS).to_html()
        assert_snapshot("toast_success", html)

    def test_accordion_snapshot(self) -> None:
        html = Accordion(items=[("FAQ", "Answer"), ("Info", "Text")], open_index=0).to_html()
        assert_snapshot("accordion", html)

    def test_dropdown_snapshot(self) -> None:
        html = Dropdown(
            label="Actions",
            items=[("Edit", "/edit"), ("Delete", "/delete")],
        ).to_html()
        assert_snapshot("dropdown", html)

    def test_select_field_snapshot(self) -> None:
        html = SelectField(
            name="role",
            label_text="Rolle",
            options=[("Admin", "admin"), ("User", "user")],
        ).to_html()
        assert_snapshot("select_field", html)

    def test_checkbox_field_snapshot(self) -> None:
        html = CheckboxField(name="agree", label_text="Ich stimme zu").to_html()
        assert_snapshot("checkbox_field", html)

    def test_radio_group_snapshot(self) -> None:
        html = RadioGroup(
            name="size",
            legend_text="Groesse",
            options=[("Small", "sm"), ("Large", "lg")],
            selected="sm",
        ).to_html()
        assert_snapshot("radio_group", html)

    def test_form_snapshot(self) -> None:
        html = Form(
            action="/submit",
            fields=[
                FormField(name="email", label_text="Email"),
            ],
        ).to_html()
        assert_snapshot("form", html)
