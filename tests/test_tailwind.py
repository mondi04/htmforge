"""Tests fuer das Tailwind-Starter-Kit ``htmforge.contrib.tailwind`` (#6)."""

from __future__ import annotations

from htmforge.contrib.tailwind import (
    Alert,
    Badge,
    Button,
    ButtonSize,
    ButtonVariant,
    Card,
    Color,
)
from htmforge.elements import p


class TestButton:
    """Tests fuer die Tailwind-``Button``-Komponente."""

    def test_primary_variant_uses_solid_background(self) -> None:
        """PRIMARY-Variante rendert eine gefuellte Hintergrundfarbe."""
        html = Button(
            label="Save", variant=ButtonVariant.PRIMARY, color=Color.BLUE
        ).to_html()
        assert "bg-blue-600" in html
        assert "text-white" in html

    def test_outline_variant_uses_border(self) -> None:
        """OUTLINE-Variante rendert eine Border statt gefuellten Hintergrund."""
        html = Button(
            label="Cancel", variant=ButtonVariant.OUTLINE, color=Color.RED
        ).to_html()
        assert "border-red-600" in html
        assert "bg-red-600" not in html

    def test_size_classes_applied(self) -> None:
        """size steuert die Padding-/Font-Size-Utility-Klassen."""
        html = Button(label="Save", size=ButtonSize.LG).to_html()
        assert "px-5 py-3 text-base" in html

    def test_default_type_is_button(self) -> None:
        """Default-type ist 'button' (kein versehentliches Form-Submit)."""
        assert 'type="button"' in Button(label="Save").to_html()

    def test_htmx_attrs_passed_through(self) -> None:
        """HTMX-Props der Basis-Component funktionieren auch hier."""
        html = Button(label="Save", hx_post="/save").to_html()
        assert 'hx-post="/save"' in html


class TestCard:
    """Tests fuer die Tailwind-``Card``-Komponente."""

    def test_renders_title_when_set(self) -> None:
        """Titel wird gerendert wenn gesetzt."""
        html = Card(title="Profile", children=[p("Body")]).to_html()
        assert "Profile" in html

    def test_no_title_element_when_empty(self) -> None:
        """Ohne title wird kein Titel-Element gerendert."""
        html = Card(children=[p("Body")]).to_html()
        assert "font-semibold" not in html

    def test_renders_element_and_string_children(self) -> None:
        """Sowohl Element- als auch String-Kinder werden gerendert."""
        html = Card(children=[p("Structured"), "Plain text"]).to_html()
        assert "Structured" in html
        assert "Plain text" in html

    def test_card_has_border_and_shadow_classes(self) -> None:
        """Card hat Border/Radius/Shadow-Utility-Klassen."""
        html = Card(children=[]).to_html()
        assert "rounded-lg" in html
        assert "shadow-sm" in html


class TestAlert:
    """Tests fuer die Tailwind-``Alert``-Komponente."""

    def test_default_color_is_red(self) -> None:
        """Default-Farbe ist RED (Fehler-Default)."""
        html = Alert(message="Something went wrong").to_html()
        assert "bg-red-50" in html
        assert "text-red-800" in html

    def test_custom_color(self) -> None:
        """Eine andere Color-Farbe wird uebernommen."""
        html = Alert(message="Saved", color=Color.GREEN).to_html()
        assert "bg-green-50" in html

    def test_role_alert_present(self) -> None:
        """role=alert ist fuer Barrierefreiheit gesetzt."""
        assert 'role="alert"' in Alert(message="Hi").to_html()


class TestBadge:
    """Tests fuer die Tailwind-``Badge``-Komponente."""

    def test_renders_text(self) -> None:
        """Badge-Text wird gerendert."""
        assert "New" in Badge(text="New").to_html()

    def test_default_color_is_slate(self) -> None:
        """Default-Farbe ist SLATE."""
        assert "bg-slate-100" in Badge(text="New").to_html()

    def test_custom_color(self) -> None:
        """Eine andere Color-Farbe wird uebernommen."""
        assert "bg-purple-100" in Badge(text="Beta", color=Color.PURPLE).to_html()
