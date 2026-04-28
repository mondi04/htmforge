"""Unit-Tests für htmforge.core.element.Element."""

from __future__ import annotations

import pytest

from htmforge.core.element import Element, _normalize_attr_name
from htmforge.elements import br, button, div, form, input, span, table, td, tr
from htmforge.htmx import HxSwap, HxTarget, HxTrigger


class TestElementRendering:
    """Tests für das grundlegende HTML-Rendering von Element."""

    def test_simple_tag_no_children(self) -> None:
        """Ein leeres Element rendert korrekt zu einem offenen und schließenden Tag."""
        el = Element("div")
        assert el.to_html() == "<div></div>"

    def test_simple_tag_with_text_child(self) -> None:
        """Ein Element mit einem Text-Kind rendert den Text korrekt."""
        el = Element("p", "Hallo Welt")
        assert el.to_html() == "<p>Hallo Welt</p>"

    def test_nested_elements(self) -> None:
        """Verschachtelte Elemente werden korrekt gerendert."""
        el = Element("div", Element("span", "Inhalt"))
        assert el.to_html() == "<div><span>Inhalt</span></div>"

    def test_multiple_children(self) -> None:
        """Mehrere Kinder werden in der richtigen Reihenfolge gerendert."""
        el = Element("ul", Element("li", "Eins"), Element("li", "Zwei"))
        assert el.to_html() == "<ul><li>Eins</li><li>Zwei</li></ul>"

    def test_none_children_are_ignored(self) -> None:
        """None-Kinder werden stillschweigend ignoriert."""
        el = Element("div", None, "Text", None)
        assert el.to_html() == "<div>Text</div>"

    def test_deeply_nested_elements(self) -> None:
        """Tief verschachtelte Strukturen (Tabelle) werden korrekt gerendert."""
        el = Element(
            "table",
            Element("tr", Element("td", "Alice"), Element("td", "alice@example.com")),
        )
        assert el.to_html() == (
            "<table><tr><td>Alice</td><td>alice@example.com</td></tr></table>"
        )


class TestVoidElements:
    """Tests für Void-Elemente (selbstschließend, kein schließender Tag)."""

    def test_input_is_void(self) -> None:
        """<input> hat keinen schließenden Tag."""
        el = Element("input", type="text")
        assert el.to_html() == '<input type="text">'

    def test_br_is_void(self) -> None:
        """<br> hat keinen schließenden Tag."""
        el = Element("br")
        assert el.to_html() == "<br>"

    def test_img_is_void(self) -> None:
        """<img> hat keinen schließenden Tag und rendert Attribute korrekt."""
        el = Element("img", src="/logo.png", alt="Logo")
        html = el.to_html()
        assert html.startswith("<img ")
        assert 'src="/logo.png"' in html
        assert 'alt="Logo"' in html
        assert not html.endswith("</img>")


class TestAttributeRendering:
    """Tests für die Attribut-Konvertierung und -Darstellung."""

    def test_cls_becomes_class(self) -> None:
        """Das ``cls``-Argument wird zu ``class`` im HTML."""
        el = Element("div", cls="container")
        assert el.to_html() == '<div class="container"></div>'

    def test_for_underscore_becomes_for(self) -> None:
        """Das ``for_``-Argument wird zu ``for`` im HTML."""
        el = Element("label", "Name", for_="name-input")
        assert el.to_html() == '<label for="name-input">Name</label>'

    def test_hx_get_becomes_hx_hyphen_get(self) -> None:
        """``hx_get`` wird zu ``hx-get``."""
        el = Element("button", "Klick", hx_get="/data")
        assert el.to_html() == '<button hx-get="/data">Klick</button>'

    def test_hx_post_becomes_hx_hyphen_post(self) -> None:
        """``hx_post`` wird zu ``hx-post``."""
        el = Element("form", hx_post="/submit")
        assert 'hx-post="/submit"' in el.to_html()

    def test_data_attribute_conversion(self) -> None:
        """``data_id`` wird zu ``data-id``."""
        el = Element("div", data_id="42")
        assert 'data-id="42"' in el.to_html()

    def test_boolean_true_attribute_is_flag_only(self) -> None:
        """Ein Attribut mit Wert ``True`` wird als Flag ohne Wert gerendert."""
        el = Element("input", type="checkbox", checked=True)
        html = el.to_html()
        assert "checked" in html
        assert 'checked="' not in html

    def test_boolean_false_attribute_is_omitted(self) -> None:
        """Ein Attribut mit Wert ``False`` wird komplett weggelassen."""
        el = Element("button", "OK", disabled=False)
        assert "disabled" not in el.to_html()

    def test_none_attribute_is_omitted(self) -> None:
        """Ein Attribut mit Wert ``None`` wird komplett weggelassen."""
        el = Element("div", data_value=None)
        assert "data-value" not in el.to_html()

    def test_multiple_attrs(self) -> None:
        """Mehrere Attribute werden korrekt gerendert."""
        el = Element("a", "Link", href="/home", cls="nav-link")
        html = el.to_html()
        assert 'href="/home"' in html
        assert 'class="nav-link"' in html

    def test_cls_list_renders_as_space_separated_class_names(self) -> None:
        """``cls`` als Liste wird als leerzeichen-separierte Klassenkette gerendert."""
        el = div("text", cls=["btn", "btn-primary"])
        assert el.to_html() == '<div class="btn btn-primary">text</div>'

    def test_enum_attribute_renders_enum_value(self) -> None:
        """Enum-Attribute werden als Enum-Value statt Enum-Name gerendert."""
        el = button("Load", hx_swap=HxSwap.OUTER_HTML)
        assert 'hx-swap="outerHTML"' in el.to_html()

    def test_enum_values_inside_list_attributes_render_values(self) -> None:
        """Enum-Werte in Listenattributen werden korrekt als Values gerendert."""
        el = div("x", data_tokens=[HxTrigger.CLICK, HxTarget.THIS])
        assert 'data-tokens="click this"' in el.to_html()


class TestXSSProtection:
    """Tests für die XSS-Sanitisierung durch markupsafe."""

    def test_text_content_is_escaped(self) -> None:
        """Potenziell gefährlicher Text-Inhalt wird HTML-escaped."""
        el = Element("p", "<script>alert('xss')</script>")
        html = el.to_html()
        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    def test_attribute_value_is_escaped(self) -> None:
        """Potenziell gefährliche Attribut-Werte werden HTML-escaped."""
        el = Element("div", cls='"><script>alert(1)</script>')
        html = el.to_html()
        assert "<script>" not in html

    def test_ampersand_in_text_is_escaped(self) -> None:
        """Kaufmännisches Und im Text wird korrekt escaped."""
        el = Element("p", "A & B")
        assert "&amp;" in el.to_html()


class TestNormalizeAttrName:
    """Unit-Tests für die ``_normalize_attr_name``-Hilfsfunktion."""

    def test_cls(self) -> None:
        """cls → class."""
        assert _normalize_attr_name("cls") == "class"

    def test_for_underscore(self) -> None:
        """for_ → for."""
        assert _normalize_attr_name("for_") == "for"

    def test_hx_get(self) -> None:
        """hx_get → hx-get."""
        assert _normalize_attr_name("hx_get") == "hx-get"

    def test_hx_swap(self) -> None:
        """hx_swap → hx-swap."""
        assert _normalize_attr_name("hx_swap") == "hx-swap"

    def test_data_foo_bar(self) -> None:
        """data_foo_bar → data-foo-bar."""
        assert _normalize_attr_name("data_foo_bar") == "data-foo-bar"

    def test_plain_name_unchanged(self) -> None:
        """Ein Name ohne Unterstriche bleibt unverändert."""
        assert _normalize_attr_name("href") == "href"


class TestElementFactories:
    """Tests fuer die Public-Factories in ``htmforge.elements``."""

    def test_basic_factories_render_expected_html(self) -> None:
        """Element-Factories liefern erwartete HTML-Ausgaben."""
        assert div("hi").to_html() == "<div>hi</div>"
        assert span("x", cls="badge").to_html() == '<span class="badge">x</span>'
        assert input(type="text", name="email").to_html() == (
            '<input type="text" name="email">'
        )
        assert br().to_html() == "<br>"

    def test_selected_requested_imports_are_usable(self) -> None:
        """Die geforderten Factory-Exporte sind direkt importierbar und nutzbar."""
        html = table(tr(td("a"))).to_html()
        assert html == "<table><tr><td>a</td></tr></table>"
        form_html = form(input(type="email"), button("Save")).to_html()
        assert "<form>" in form_html


class TestNewElementFactories:
    """Tests fuer die neuen Element-Factories aus Block D / v0.2.0."""

    def test_dialog_factory(self) -> None:
        from htmforge.elements import dialog

        assert dialog("Inhalt").to_html() == "<dialog>Inhalt</dialog>"

    def test_details_summary_factory(self) -> None:
        from htmforge.elements import details, summary

        html = details(summary("Titel"), "Text").to_html()
        assert html == "<details><summary>Titel</summary>Text</details>"

    def test_fieldset_legend_factory(self) -> None:
        from htmforge.elements import fieldset, legend

        html = fieldset(legend("Gruppe")).to_html()
        assert "<fieldset>" in html
        assert "<legend>Gruppe</legend>" in html

    def test_progress_is_not_void(self) -> None:
        from htmforge.elements import progress

        html = progress(value="50", max="100").to_html()
        assert html == '<progress value="50" max="100"></progress>'

    def test_col_is_void(self) -> None:
        from htmforge.elements import col

        html = col(span="2").to_html()
        assert html == '<col span="2">'
        assert "</col>" not in html

    def test_audio_video_factories(self) -> None:
        from htmforge.elements import audio, source, video

        html = video(source(src="/v.mp4", type="video/mp4"), controls=True).to_html()
        assert "controls" in html
        assert '<source src="/v.mp4"' in html

    def test_map_factory_renders_map_tag(self) -> None:
        from htmforge.elements import map_

        html = map_(name="nav").to_html()
        assert html == '<map name="nav"></map>'

    def test_mark_kbd_abbr_time_small(self) -> None:
        from htmforge.elements import abbr, kbd, mark, small, time

        assert mark("wichtig").to_html() == "<mark>wichtig</mark>"
        assert kbd("Ctrl+C").to_html() == "<kbd>Ctrl+C</kbd>"
        assert abbr("HTML", title="HyperText").to_html() == '<abbr title="HyperText">HTML</abbr>'
        assert time("2026", datetime="2026-01-01").to_html() == '<time datetime="2026-01-01">2026</time>'
        assert small("Hinweis").to_html() == "<small>Hinweis</small>"
