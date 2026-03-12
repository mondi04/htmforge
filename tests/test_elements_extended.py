"""Tests fuer neue Element-Features: safe_html, __str__ und Head-Elemente."""

from __future__ import annotations

from markupsafe import Markup

from htmlkit.core.element import Element, safe_html
from htmlkit.elements import (
    body,
    div,
    head,
    html,
    link,
    meta,
    noscript,
    raw,
    script,
    span,
    style,
    title,
)


class TestSafeHtml:
    """Tests fuer die ``safe_html``-Funktion."""

    def test_html_tags_are_not_escaped(self) -> None:
        """HTML-Tags in safe_html werden nicht escaped."""
        el = div(safe_html("<strong>fett</strong>"))
        assert el.to_html() == "<div><strong>fett</strong></div>"

    def test_safe_html_returns_markup_instance(self) -> None:
        """``safe_html`` gibt ein ``Markup``-Objekt zurueck."""
        result = safe_html("<em>x</em>")
        assert isinstance(result, Markup)

    def test_plain_string_is_still_escaped(self) -> None:
        """Rohe Strings ohne safe_html werden weiterhin escaped."""
        el = div("<script>evil()</script>")
        assert "<script>" not in el.to_html()
        assert "&lt;script&gt;" in el.to_html()

    def test_safe_html_mixed_with_elements(self) -> None:
        """safe_html und normale Strings koennen kombiniert werden."""
        el = div(safe_html("<b>bold</b>"), " & plain")
        html_out = el.to_html()
        assert "<b>bold</b>" in html_out
        assert "&amp;" in html_out


class TestElementDunderStr:
    """Tests fuer ``Element.__str__``."""

    def test_str_equals_to_html(self) -> None:
        """``str(el)`` liefert dasselbe Ergebnis wie ``el.to_html()``."""
        el = div(span("Hallo"), cls="container")
        assert str(el) == el.to_html()

    def test_str_can_be_used_in_f_string(self) -> None:
        """Elemente koennen direkt in f-Strings verwendet werden."""
        el = span("World")
        result = f"Hello {el}"
        assert result == "Hello <span>World</span>"


class TestRawHelper:
    """Tests fuer die ``raw``-Hilfsfunktion in ``htmlkit.elements``."""

    def test_raw_returns_markup(self) -> None:
        """``raw()`` gibt ein ``Markup``-Objekt zurueck."""
        assert isinstance(raw("x"), Markup)

    def test_script_with_raw_content_not_escaped(self) -> None:
        """JavaScript in ``script(raw(...))`` wird nicht escaped."""
        el = script(raw("console.log('hello & world');"))
        html_out = el.to_html()
        assert "console.log('hello &amp; world');" not in html_out
        assert "console.log('hello & world');" in html_out

    def test_style_with_raw_content_not_escaped(self) -> None:
        """CSS in ``style(raw(...))`` wird nicht escaped."""
        css = "a > b { color: red; }"
        el = style(raw(css))
        html_out = el.to_html()
        assert "a &gt; b" not in html_out
        assert css in html_out


class TestNewDocumentElements:
    """Tests fuer die neuen Dokument-Struktur-Elemente."""

    def test_html_element(self) -> None:
        """``html()`` rendert einen ``<html>``-Tag."""
        assert html().to_html() == "<html></html>"

    def test_head_element(self) -> None:
        """``head()`` rendert einen ``<head>``-Tag."""
        assert head().to_html() == "<head></head>"

    def test_body_element(self) -> None:
        """``body()`` rendert einen ``<body>``-Tag."""
        assert body().to_html() == "<body></body>"

    def test_title_element(self) -> None:
        """``title()`` rendert einen ``<title>``-Tag mit Inhalt."""
        assert title("Seite").to_html() == "<title>Seite</title>"

    def test_title_content_is_escaped(self) -> None:
        """Text in ``title()`` wird weiterhin escaped."""
        el = title("<evil>")
        assert "&lt;evil&gt;" in el.to_html()

    def test_meta_is_void(self) -> None:
        """``meta()`` hat keinen schliessenden Tag."""
        el = meta(charset="utf-8")
        assert el.to_html() == '<meta charset="utf-8">'

    def test_link_is_void(self) -> None:
        """``link()`` hat keinen schliessenden Tag."""
        el = link(rel="stylesheet", href="/style.css")
        html_out = el.to_html()
        assert html_out.startswith("<link ")
        assert not html_out.endswith("</link>")
        assert 'rel="stylesheet"' in html_out

    def test_script_with_src(self) -> None:
        """``script(src=...)`` rendert externes Skript korrekt."""
        el = script(src="/app.js")
        assert el.to_html() == '<script src="/app.js"></script>'

    def test_noscript_element(self) -> None:
        """``noscript()`` rendert Fallback-Inhalt."""
        el = noscript("JavaScript benoetigt")
        assert el.to_html() == "<noscript>JavaScript benoetigt</noscript>"
