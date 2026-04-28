"""Unit-Tests fuer vorgefertigte Komponenten in ``htmforge.components``."""

from __future__ import annotations

import importlib

from htmforge.components import (
    Alert,
    AlertVariant,
    Badge,
    BadgeVariant,
    Breadcrumb,
    DataTable,
    Modal,
    Pagination,
    SearchInput,
)
from htmforge.components.form_field import FormField, InputType
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import li, ul


class TestDataTable:
    """Tests fuer die ``DataTable``-Komponente."""

    def test_render_basic_table_structure(self) -> None:
        """Rendert ``thead`` und ``tbody`` mit Headern und Zeilen."""
        table_component = DataTable(
            headers=["Name", "Rolle"],
            rows=[["Ada", "Admin"], ["Grace", "User"]],
        )

        html = table_component.to_html()

        assert html.startswith('<div class="table-wrapper"><table class="table"')
        assert "<thead><tr><th>Name</th><th>Rolle</th></tr></thead>" in html
        assert "<tbody>" in html
        assert "<tr><td>Ada</td><td>Admin</td></tr>" in html
        assert "<tr><td>Grace</td><td>User</td></tr>" in html

    def test_render_empty_rows_shows_message_with_colspan(self) -> None:
        """Wenn keine Zeilen vorhanden sind, wird die Empty-Zeile gerendert."""
        table_component = DataTable(headers=["Name", "Rolle"], rows=[])

        html = table_component.to_html()

        assert '<td colspan="2" class="table__empty">Keine Einträge</td>' in html

    def test_datatable_empty_rows(self) -> None:
        """Leere Tabellen zeigen den Empty-State mit ``table__empty``."""
        table_component = DataTable(headers=["Name"], rows=[])
        html = table_component.to_html()
        assert 'class="table-wrapper"' in html
        assert 'class="table"' in html
        assert '<td colspan="1" class="table__empty">Keine Einträge</td>' in html

    def test_render_sets_htmx_attributes_when_hx_url_is_configured(self) -> None:
        """Optionales Reloading per HTMX wird auf ``table`` gesetzt."""
        table_component = DataTable(
            headers=["Name"],
            rows=[["Ada"]],
            hx_url="/api/users/table",
        )

        html = table_component.to_html()

        assert 'hx-get="/api/users/table"' in html
        assert 'hx-trigger="load"' in html


class TestAlert:
    """Tests fuer die ``Alert``-Komponente."""

    def test_render_basic_alert_variant_class(self) -> None:
        """Variant wird als CSS-Klasse auf das Root-Div geschrieben."""
        alert = Alert(message="Gespeichert", variant=AlertVariant.SUCCESS)

        html = alert.to_html()

        assert html == '<div class="alert alert-success">Gespeichert</div>'

    def test_render_dismissible_alert_adds_js_close_button(self) -> None:
        """Dismissible Alerts enthalten einen JS-Close-Button."""
        alert = Alert(message="Hinweis", dismissible=True)

        html = alert.to_html()

        assert "<button" in html
        assert "×" in html
        assert "onclick=\"this.closest(&#39;.alert&#39;).remove()\"" in html
        assert "hx-get" not in html

    def test_render_non_dismissible_has_no_close_button(self) -> None:
        """Ohne ``dismissible`` wird kein Button gerendert."""
        alert = Alert(message="Nur Info")

        html = alert.to_html()

        assert "<button" not in html


class TestPagination:
    """Tests fuer die ``Pagination``-Komponente."""

    def test_render_basic_pagination_structure(self) -> None:
        """Rendert alle Seiten sowie Previous/Next-Links."""
        pager = Pagination(
            current_page=2,
            total_pages=3,
            hx_url="/users?page={page}",
            hx_target="#users-list",
        )

        html = pager.to_html()

        assert html.startswith('<ul class="pagination">')
        assert '<li class="active"><a href="#">2</a></li>' in html
        assert 'hx-get="/users?page=1"' in html
        assert 'hx-get="/users?page=3"' in html
        assert 'hx-target="#users-list"' in html

    def test_render_first_page_disables_previous_and_enables_next(self) -> None:
        """Auf Seite 1 ist Previous deaktiviert und Next aktiv."""
        pager = Pagination(
            current_page=1,
            total_pages=3,
            hx_url="/users?page={page}",
            hx_target="#users-list",
        )

        html = pager.to_html()

        assert '<li class="disabled"><a href="#">Previous</a></li>' in html
        assert 'hx-get="/users?page=2"' in html

    def test_render_last_page_disables_next_and_enables_previous(self) -> None:
        """Auf letzter Seite ist Next deaktiviert und Previous aktiv."""
        pager = Pagination(
            current_page=3,
            total_pages=3,
            hx_url="/users?page={page}",
            hx_target="#users-list",
        )

        html = pager.to_html()

        assert '<li class="disabled"><a href="#">Next</a></li>' in html
        assert 'hx-get="/users?page=2"' in html

    def test_render_with_default_hx_target_omits_hx_target_attribute(self) -> None:
        """Wenn ``hx_target`` leer ist, wird kein ``hx-target`` gerendert."""
        pager = Pagination(
            current_page=2,
            total_pages=3,
            hx_url="/users?page={page}",
        )

        html = pager.to_html()

        assert 'hx-get="/users?page=1"' in html
        assert 'hx-get="/users?page=3"' in html
        assert "hx-target=" not in html

    def test_pagination_no_hx_target(self) -> None:
        """Ohne ``hx_target`` wird kein ``hx-target`` Attribut gerendert."""
        pager = Pagination(current_page=2, total_pages=4, hx_url="/x?page={page}")
        html = pager.to_html()
        assert 'hx-get="/x?page=1"' in html
        assert 'hx-get="/x?page=3"' in html
        assert "hx-target=" not in html


class TestBadge:
    """Tests fuer die ``Badge``-Komponente."""

    def test_render_default_variant(self) -> None:
        """Ohne Variante wird die Default-Klasse gerendert."""
        html = Badge(text="Neu").to_html()
        assert html == '<span class="badge badge-default">Neu</span>'

    def test_render_danger_variant(self) -> None:
        """Die Danger-Variante wird korrekt als CSS-Klasse gerendert."""
        html = Badge(text="3", variant=BadgeVariant.DANGER).to_html()
        assert html == '<span class="badge badge-danger">3</span>'

    def test_text_content_is_escaped(self) -> None:
        """Badge-Text wird sicher escaped."""
        html = Badge(text="<b>").to_html()
        assert "&lt;b&gt;" in html


class TestBreadcrumb:
    """Tests fuer die ``Breadcrumb``-Komponente."""

    def test_render_links_for_non_current_items(self) -> None:
        """Nicht-aktuelle Items werden als Links gerendert."""
        html = Breadcrumb(items=[("Home", "/"), ("Produkte", "/produkte"), ("Detail", None)]).to_html()
        assert '<a href="/">Home</a>' in html
        assert '<a href="/produkte">Produkte</a>' in html

    def test_render_span_for_current_item(self) -> None:
        """Das aktuelle Item wird als Span mit aria-current gerendert."""
        html = Breadcrumb(items=[("Home", "/"), ("Aktuell", None)]).to_html()
        assert '<span aria-current="page">Aktuell</span>' in html

    def test_single_item_renders_as_current(self) -> None:
        """Ein einzelnes Item wird als aktuelles Element gerendert."""
        html = Breadcrumb(items=[("Aktuell", None)]).to_html()
        assert 'class="breadcrumb-item active"' in html

    def test_aria_label_present(self) -> None:
        """Die Navigation hat ein aria-label."""
        html = Breadcrumb(items=[("Home", "/")]).to_html()
        assert 'aria-label="breadcrumb"' in html


class TestSearchInput:
    """Tests fuer die ``SearchInput``-Komponente."""

    def test_render_debounce_trigger(self) -> None:
        """Standardmaessig wird ein 300ms Debounce gerendert."""
        html = SearchInput(
            name="q",
            search_url="/search",
            search_target="#results",
        ).to_html()
        assert 'hx-trigger="keyup delay:300ms"' in html

    def test_custom_debounce_ms(self) -> None:
        """Ein benutzerdefinierter Debounce wird im Trigger sichtbar."""
        html = SearchInput(
            name="q",
            search_url="/search",
            search_target="#results",
            debounce_ms=500,
        ).to_html()
        assert "500ms" in html

    def test_hx_get_and_target_present(self) -> None:
        """hx-get und hx-target werden im Input gerendert."""
        html = SearchInput(
            name="q",
            search_url="/search",
            search_target="#results",
        ).to_html()
        assert 'hx-get="/search"' in html
        assert 'hx-target="#results"' in html

    def test_indicator_attribute_when_set(self) -> None:
        """Ein Indicator wird als hx-indicator gerendert."""
        html = SearchInput(
            name="q",
            search_url="/search",
            search_target="#results",
            indicator="#spinner",
        ).to_html()
        assert 'hx-indicator="#spinner"' in html

    def test_indicator_absent_when_empty(self) -> None:
        """Ohne Indicator wird kein hx-indicator gerendert."""
        html = SearchInput(
            name="q",
            search_url="/search",
            search_target="#results",
        ).to_html()
        assert "hx-indicator=" not in html


class TestModal:
    """Tests fuer die ``Modal``-Komponente."""

    def test_trigger_button_has_hx_get(self) -> None:
        """Der Trigger-Button laedt den Inhalt per HTMX."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
        ).to_html()
        assert 'hx-get="/modal/content"' in html

    def test_trigger_uses_data_modal_target(self) -> None:
        """Der Trigger nutzt ein data-Attribut statt onclick-JavaScript."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
        ).to_html()
        assert 'data-modal-target="confirm"' in html

    def test_inline_script_present(self) -> None:
        """Das Inline-Script zum Oeffnen des Dialogs ist vorhanden."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
        ).to_html()
        assert "<script>" in html
        assert "showModal" in html

    def test_dialog_id_matches_modal_id(self) -> None:
        """Das dialog-Element verwendet modal_id als id."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
        ).to_html()
        assert '<dialog id="confirm" class="modal">' in html

    def test_body_div_id_is_derived_from_modal_id(self) -> None:
        """Die Body-Div-ID wird aus modal_id abgeleitet."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
        ).to_html()
        assert '<div id="confirm-body" class="modal-body"></div>' in html

    def test_close_button_in_form_with_method_dialog(self) -> None:
        """Der Close-Button sitzt in einem form method=dialog."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
        ).to_html()
        assert 'method="dialog"' in html
        assert '<button class="modal-close">Schließen</button>' in html

    def test_custom_close_label(self) -> None:
        """Der Close-Button nutzt ein benutzerdefiniertes Label."""
        html = Modal(
            modal_id="confirm",
            trigger_label="Öffnen",
            hx_url="/modal/content",
            close_label="Cerrar",
        ).to_html()
        assert '<button class="modal-close">Cerrar</button>' in html


class TestPublicExports:
    """Tests fuer Public-Exports im Package-Root."""

    def test_components_exports_block_d_symbols(self) -> None:
        """Die Block-D-Symbole sind aus ``htmforge.components`` importierbar."""
        module = importlib.import_module("htmforge.components")
        for symbol in ("Badge", "BadgeVariant", "Breadcrumb", "Modal", "SearchInput"):
            assert hasattr(module, symbol)

    def test_page_not_exported_from_components(self) -> None:
        """Page bleibt bewusst nicht aus ``htmforge.components`` exportiert."""
        module = importlib.import_module("htmforge.components")
        assert not hasattr(module, "Page")


# ---------------------------------------------------------------------------
# Fixture-Subklassen für Page
# ---------------------------------------------------------------------------


class SimplePage(Page):
    """Minimale Page-Subklasse fuer Tests."""

    content: str = ""

    def _body_content(self) -> list[Element | str | None]:
        return [ul(li(self.content))] if self.content else []


# ---------------------------------------------------------------------------
# Tests: Page
# ---------------------------------------------------------------------------


class TestPage:
    """Tests fuer die ``Page``-Komponente."""

    def test_to_html_starts_with_doctype(self) -> None:
        """Die Ausgabe beginnt mit ``<!DOCTYPE html>``."""
        page = SimplePage(title="Test")
        assert page.to_html().startswith("<!DOCTYPE html>")

    def test_title_in_head(self) -> None:
        """Der Dokumenttitel erscheint im ``<title>``-Tag."""
        page = SimplePage(title="Meine Seite")
        html_out = page.to_html()
        assert "<title>Meine Seite</title>" in html_out

    def test_css_url_renders_link_stylesheet(self) -> None:
        """``css_urls`` erzeugt einen ``<link rel=\"stylesheet\">``-Tag."""
        page = SimplePage(title="X", css_urls=["/static/main.css"])
        html_out = page.to_html()
        assert 'rel="stylesheet"' in html_out
        assert 'href="/static/main.css"' in html_out

    def test_js_url_renders_script_at_end_of_body(self) -> None:
        """``js_urls`` erzeugt einen ``<script src=...>``-Tag vor ``</body>``."""
        page = SimplePage(title="X", js_urls=["/static/app.js"])
        html_out = page.to_html()
        script_pos = html_out.index('<script src="/static/app.js">')
        body_close_pos = html_out.index("</body>")
        assert script_pos < body_close_pos

    def test_inline_css_not_escaped(self) -> None:
        """Inline-CSS in ``<style>`` wird nicht escaped."""
        css = "body { color: red; }"
        page = SimplePage(title="X", inline_css=css)
        html_out = page.to_html()
        assert f"<style>{css}</style>" in html_out

    def test_description_renders_meta_tag(self) -> None:
        """``description`` erzeugt ein ``<meta name=\"description\">``-Tag."""
        page = SimplePage(title="X", description="Seiten-Beschreibung")
        html_out = page.to_html()
        assert 'name="description"' in html_out
        assert 'content="Seiten-Beschreibung"' in html_out

    def test_no_description_omits_meta_tag(self) -> None:
        """Ohne ``description`` wird kein entsprechendes Meta-Tag gerendert."""
        page = SimplePage(title="X")
        assert 'name="description"' not in page.to_html()

    def test_charset_meta_present(self) -> None:
        """Das ``charset``-Meta-Tag ist immer vorhanden."""
        page = SimplePage(title="X")
        assert 'charset="utf-8"' in page.to_html()

    def test_render_returns_html_element_without_doctype(self) -> None:
        """``render()`` gibt ein ``<html>``-Element ohne DOCTYPE zurueck."""
        page = SimplePage(title="X")
        el = page.render()
        assert el.to_html().startswith("<html>")


# ---------------------------------------------------------------------------
# Tests: FormField
# ---------------------------------------------------------------------------


class TestFormField:
    """Tests fuer die ``FormField``-Komponente."""

    def test_render_label_and_input_linked_by_id(self) -> None:
        """``for``-Attribut des Labels und ``id`` des Inputs stimmen ueberein."""
        field = FormField(name="email", label_text="E-Mail")
        html_out = field.to_html()
        assert 'for="email"' in html_out
        assert 'id="email"' in html_out

    def test_required_attribute_set_when_true(self) -> None:
        """``required=True`` setzt das ``required``-Flag auf dem Input."""
        field = FormField(name="pwd", label_text="Passwort", required=True)
        html_out = field.to_html()
        assert "required" in html_out
        assert 'aria-required="true"' in html_out

    def test_required_attribute_absent_when_false(self) -> None:
        """Ohne ``required=True`` erscheint kein required-Attribut."""
        field = FormField(name="note", label_text="Notiz")
        html_out = field.to_html()
        assert "required" not in html_out
        assert "aria-required" not in html_out

    def test_form_field_required(self) -> None:
        """``required=True`` setzt required und aria-required auf Label und Input."""
        field = FormField(name="mail", label_text="Mail", required=True)
        html_out = field.to_html()
        assert "required" in html_out
        assert html_out.count('aria-required="true"') == 2

    def test_form_field_not_required(self) -> None:
        """Default ohne required rendert keine Required-Attribute."""
        field = FormField(name="mail", label_text="Mail")
        html_out = field.to_html()
        assert "required" not in html_out
        assert "aria-required" not in html_out

    def test_error_renders_error_div(self) -> None:
        """``error`` erzeugt ein ``<div class=\"field-error\">``."""
        field = FormField(name="x", label_text="X", error="Pflichtfeld")
        html_out = field.to_html()
        assert 'class="field-error"' in html_out
        assert "Pflichtfeld" in html_out

    def test_no_error_omits_error_div(self) -> None:
        """Ohne Fehler wird kein Error-Div gerendert."""
        field = FormField(name="x", label_text="X")
        assert "field-error" not in field.to_html()

    def test_field_id_generated_from_name_when_empty(self) -> None:
        """Wenn ``field_id`` leer ist, wird die ID aus ``name`` abgeleitet."""
        field = FormField(name="first name", label_text="Vorname")
        html_out = field.to_html()
        assert 'id="first-name"' in html_out
        assert 'for="first-name"' in html_out

    def test_explicit_field_id_used_when_set(self) -> None:
        """Ein explizit gesetztes ``field_id`` wird uebernommen."""
        field = FormField(name="email", label_text="E-Mail", field_id="user-email")
        html_out = field.to_html()
        assert 'id="user-email"' in html_out
        assert 'for="user-email"' in html_out

    def test_input_type_email_renders_correctly(self) -> None:
        """``InputType.EMAIL`` setzt ``type=\"email\"`` am Input."""
        field = FormField(
            name="mail",
            label_text="Mail",
            input_type=InputType.EMAIL,
        )
        assert 'type="email"' in field.to_html()
