"""Unit-Tests für htmlkit.core.component.Component."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from htmlkit.core.component import Component
from htmlkit.core.element import Element
from htmlkit.elements import button, div, p, span, table, td, tr


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


# ---------------------------------------------------------------------------
# Tests: Struktur / Vererbung
# ---------------------------------------------------------------------------


class TestComponentInheritance:
    """Tests für die Klassen-Hierarchie und abstrakte Interface-Anforderungen."""

    def test_component_without_render_cannot_be_instantiated(self) -> None:
        """Eine Subklasse ohne ``render()`` kann nicht instanziiert werden."""

        class IncompleteComponent(Component):
            value: str

        with pytest.raises(TypeError):
            IncompleteComponent(value="test")  # type: ignore[abstract]

    def test_render_must_return_element(self) -> None:
        """``render()`` gibt ein :class:`~htmlkit.core.element.Element` zurück."""
        card = GreetingCard(title="Test")
        result = card.render()
        assert isinstance(result, Element)
