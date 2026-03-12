"""Unit-Tests für htmforge.core.component.Component."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from htmforge import Component as PublicComponent
from htmforge import Element as PublicElement
from htmforge.core.component import Component
from htmforge.core.element import Element
from htmforge.elements import button, div, p, span, table, td, tr
from htmforge.htmx import HxPushUrl, HxSwap, HxTarget, HxTrigger


# ---------------------------------------------------------------------------
# Fixture-Komponenten
# ---------------------------------------------------------------------------


class GreetingCard(Component):
    """Einfache Test-Komponente mit einem Titel und einem optionalen Body."""

    title: str
    body: str = "Kein Inhalt"

    def render(self) -> Element:
        """Rendert eine Karte mit Titel und Body."""
        return div(p(self.title), p(self.body), cls="card")


class UserRow(Component):
    """Tabellenzeile für einen einzelnen Benutzer."""

    name: str
    email: str
    show_email: bool = True

    def render(self) -> Element:
        """Rendert eine Tabellenzeile mit Name und optionaler E-Mail."""
        cells: list[Element | str | None] = [td(self.name)]
        if self.show_email:
            cells.append(td(self.email))
        else:
            cells.append(td("***"))
        return tr(*cells)


class Counter(Component):
    """Komponente mit Integer-Prop und HTMX-Button."""

    count: int

    def render(self) -> Element:
        """Rendert einen HTMX-gesteuerten Inkrementier-Button."""
        return div(
            span(str(self.count), id="counter-value"),
            button(
                "+1",
                hx_post="/increment",
                hx_target="#counter-value",
                hx_swap="innerHTML",
            ),
        )


class HtmxDeleteButton(Component):
    """Komponente, die HTMX-Props aus dem Basismodell nutzt."""

    label: str = "Delete"

    def render(self) -> Element:
        """Rendert einen Button mit allen gesetzten HTMX-Attributen."""
        return button(self.label, **self.htmx_attrs())


# ---------------------------------------------------------------------------
# Tests: Rendering
# ---------------------------------------------------------------------------


class TestComponentRendering:
    """Tests für das HTML-Rendering von Komponenten."""

    def test_to_html_delegates_to_render(self) -> None:
        """``to_html()`` delegiert korrekt an ``render()``."""
        card = GreetingCard(title="Hallo", body="Welt")
        expected = '<div class="card"><p>Hallo</p><p>Welt</p></div>'
        assert card.to_html() == expected

    def test_default_prop_is_used(self) -> None:
        """Default-Werte von Props werden korrekt gerendert."""
        card = GreetingCard(title="Nur Titel")
        assert "Kein Inhalt" in card.to_html()

    def test_conditional_rendering(self) -> None:
        """Bedingte Darstellung (show_email=False) rendert den Ersatz."""
        row = UserRow(name="Alice", email="alice@example.com", show_email=False)
        html = row.to_html()
        assert "***" in html
        assert "alice@example.com" not in html

    def test_conditional_rendering_shows_email_by_default(self) -> None:
        """Default-Verhalten zeigt die E-Mail-Adresse an."""
        row = UserRow(name="Bob", email="bob@example.com")
        assert "bob@example.com" in row.to_html()

    def test_integer_prop_renders_as_string(self) -> None:
        """Integer-Props werden korrekt zu Text konvertiert."""
        counter = Counter(count=42)
        assert "42" in counter.to_html()

    def test_htmx_attrs_in_component(self) -> None:
        """HTMX-Attribute in der render()-Methode werden korrekt konvertiert."""
        counter = Counter(count=0)
        html = counter.to_html()
        assert 'hx-post="/increment"' in html
        assert 'hx-target="#counter-value"' in html
        assert 'hx-swap="innerHTML"' in html

    def test_typed_htmx_props_render_via_helper(self) -> None:
        """Typisierte HTMX-Props werden ueber ``htmx_attrs`` korrekt gerendert."""
        component = HtmxDeleteButton(
            hx_delete="/users/1",
            hx_swap=HxSwap.OUTER_HTML,
            hx_target=HxTarget.THIS,
            hx_trigger=HxTrigger.CLICK,
            hx_push_url=HxPushUrl.FALSE,
        )
        html = component.to_html()
        assert 'hx-delete="/users/1"' in html
        assert 'hx-swap="outerHTML"' in html
        assert 'hx-target="this"' in html
        assert 'hx-trigger="click"' in html
        assert 'hx-push-url="false"' in html

    def test_htmx_attrs_omits_none_values(self) -> None:
        """``htmx_attrs`` gibt nur gesetzte Werte zurueck."""
        component = HtmxDeleteButton(hx_post="/submit")
        attrs = component.htmx_attrs()
        assert attrs == {"hx_post": "/submit"}

    def test_htmx_attrs_serializes_mapping_values(self) -> None:
        """Mapping-Werte werden in `htmx_attrs` als JSON serialisiert."""
        component = HtmxDeleteButton(
            hx_headers={"X-CSRF": "token"},
            hx_request={"timeout": 1000},
            hx_vals={"id": 42},
        )
        attrs = component.htmx_attrs()
        assert attrs["hx_headers"] == '{"X-CSRF":"token"}'
        assert attrs["hx_request"] == '{"timeout":1000}'
        assert attrs["hx_vals"] == '{"id":42}'

    def test_extended_htmx_props_render_via_helper(self) -> None:
        """Erweiterte HTMX-Props erscheinen korrekt im gerenderten HTML."""
        component = HtmxDeleteButton(
            hx_select="#row",
            hx_select_oob="#flash",
            hx_params="*",
            hx_encoding="multipart/form-data",
            hx_headers={"X-CSRF": "token"},
        )
        html = component.to_html()
        assert 'hx-select="#row"' in html
        assert 'hx-select-oob="#flash"' in html
        assert 'hx-params="*"' in html
        assert 'hx-encoding="multipart/form-data"' in html
        assert "hx-headers=" in html

    def test_component_usable_as_child_of_element(self) -> None:
        """Eine Komponente kann direkt als Kind eines Elements verwendet werden."""
        card = GreetingCard(title="Nested", body="Test")
        wrapper = div(card)
        html = wrapper.to_html()
        assert '<div class="card">' in html
        assert "Nested" in html


# ---------------------------------------------------------------------------
# Tests: Props-Validierung (Pydantic V2)
# ---------------------------------------------------------------------------


class TestComponentPropsValidation:
    """Tests für die Pydantic-Props-Validierung."""

    def test_missing_required_field_raises_validation_error(self) -> None:
        """Fehlende Pflicht-Props lösen einen ``ValidationError`` aus."""
        with pytest.raises(ValidationError):
            GreetingCard()  # type: ignore[call-arg]

    def test_wrong_type_raises_validation_error(self) -> None:
        """Falsche Types bei Props lösen einen ``ValidationError`` aus."""
        with pytest.raises(ValidationError):
            Counter(count="keine-zahl")  # type: ignore[arg-type]

    def test_valid_props_do_not_raise(self) -> None:
        """Korrekte Props lösen keinen Fehler aus."""
        card = GreetingCard(title="OK", body="Alles gut")
        assert card.title == "OK"

    def test_validate_assignment_on_mutation(self) -> None:
        """``validate_assignment=True``: Zuweisung eines falschen Typs löst Fehler aus."""
        counter = Counter(count=5)
        with pytest.raises(ValidationError):
            counter.count = "falsch"  # type: ignore[assignment]

    def test_pydantic_coercion_int_from_string(self) -> None:
        """Pydantic koerziert kompatible Typen (str → int)."""
        counter = Counter(count="7")  # type: ignore[arg-type]
        assert counter.count == 7

    def test_invalid_typed_htmx_prop_raises_validation_error(self) -> None:
        """Falsche Typen fuer typisierte HTMX-Props werden abgelehnt."""
        with pytest.raises(ValidationError):
            HtmxDeleteButton(hx_swap=123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Tests: Struktur / Vererbung
# ---------------------------------------------------------------------------


class TestComponentInheritance:
    """Tests für die Klassen-Hierarchie und abstrakte Interface-Anforderungen."""

    def test_no_render_component_raises_type_error(self) -> None:
        """Eine Klasse ohne ``render()`` wirft beim Instanziieren einen TypeError."""

        class NoRender(Component):
            pass

        with pytest.raises(TypeError):
            NoRender()  # type: ignore[abstract]

    def test_component_without_render_cannot_be_instantiated(self) -> None:
        """Eine Subklasse ohne ``render()`` kann nicht instanziiert werden."""

        class IncompleteComponent(Component):
            value: str

        with pytest.raises(TypeError):
            IncompleteComponent(value="test")  # type: ignore[abstract]

    def test_render_must_return_element(self) -> None:
        """``render()`` gibt ein :class:`~htmforge.core.element.Element` zurück."""
        card = GreetingCard(title="Test")
        result = card.render()
        assert isinstance(result, Element)


class TestPublicExports:
    """Tests fuer Public-Exports im Package-Root."""

    def test_root_exports_component_and_element(self) -> None:
        """Das Root-Package exportiert ``Component`` und ``Element``."""
        assert PublicComponent is Component
        assert PublicElement is Element
