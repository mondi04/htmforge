"""Vordefinierte HTML-Elemente für htmlkit.

Exportiert Convenience-Funktionen für alle gängigen HTML-Tags.
Jede Funktion ist eine dünne Factory, die ein :class:`~htmlkit.core.element.Element`
mit dem entsprechenden Tag-Namen erstellt.

Naming-Konventionen:
    - ``cls`` statt ``class`` (Python-Keyword-Konflikt).
    - ``for_`` statt ``for`` (Python-Keyword-Konflikt).
    - HTMX-Attribute als ``hx_get``, ``hx_post`` etc. (werden automatisch
      zu ``hx-get``, ``hx-post`` konvertiert).

Example::

    from htmlkit.elements import div, table, tr, td, button

    layout = div(
        table(
            tr(td("Alice"), td("alice@example.com")),
            tr(td("Bob"),   td("bob@example.com")),
        ),
        cls="container",
    )
    print(layout.to_html())
"""

from __future__ import annotations

from htmlkit.core.element import Child, Element

# ---------------------------------------------------------------------------
# Text / Inline
# ---------------------------------------------------------------------------


def span(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<span>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``span``.
    """
    return Element("span", *children, **attrs)


def p(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<p>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``p``.
    """
    return Element("p", *children, **attrs)


def a(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<a>``-Element (Hyperlink).

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute (z.B. ``href``, ``target``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``a``.
    """
    return Element("a", *children, **attrs)


def strong(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<strong>``-Element (fetter Text).

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``strong``.
    """
    return Element("strong", *children, **attrs)


def em(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<em>``-Element (kursiver Text).

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``em``.
    """
    return Element("em", *children, **attrs)


# ---------------------------------------------------------------------------
# Block / Layout
# ---------------------------------------------------------------------------


def div(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<div>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute (z.B. ``cls``, ``id``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``div``.
    """
    return Element("div", *children, **attrs)


def section(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<section>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``section``.
    """
    return Element("section", *children, **attrs)


def article(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<article>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``article``.
    """
    return Element("article", *children, **attrs)


def header(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<header>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``header``.
    """
    return Element("header", *children, **attrs)


def footer(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<footer>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``footer``.
    """
    return Element("footer", *children, **attrs)


def main(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<main>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``main``.
    """
    return Element("main", *children, **attrs)


def nav(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<nav>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``nav``.
    """
    return Element("nav", *children, **attrs)


# ---------------------------------------------------------------------------
# Headings
# ---------------------------------------------------------------------------


def h1(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<h1>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``h1``.
    """
    return Element("h1", *children, **attrs)


def h2(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<h2>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``h2``.
    """
    return Element("h2", *children, **attrs)


def h3(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<h3>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``h3``.
    """
    return Element("h3", *children, **attrs)


# ---------------------------------------------------------------------------
# Interactive
# ---------------------------------------------------------------------------


def button(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<button>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute (z.B. ``type``, ``disabled``,
            ``hx_post``, ``hx_swap``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``button``.
    """
    return Element("button", *children, **attrs)


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


def table(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<table>``-Element.

    Args:
        *children: Kind-Elemente (i.d.R. ``thead``, ``tbody``, ``tr``).
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``table``.
    """
    return Element("table", *children, **attrs)


def thead(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<thead>``-Element.

    Args:
        *children: Kind-Elemente.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``thead``.
    """
    return Element("thead", *children, **attrs)


def tbody(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<tbody>``-Element.

    Args:
        *children: Kind-Elemente.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``tbody``.
    """
    return Element("tbody", *children, **attrs)


def tr(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<tr>``-Element (Tabellenzeile).

    Args:
        *children: Kind-Elemente (``td``, ``th``).
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``tr``.
    """
    return Element("tr", *children, **attrs)


def td(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<td>``-Element (Tabellenzelle).

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute (z.B. ``colspan``, ``rowspan``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``td``.
    """
    return Element("td", *children, **attrs)


def th(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<th>``-Element (Tabellen-Header-Zelle).

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute (z.B. ``scope``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``th``.
    """
    return Element("th", *children, **attrs)


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------


def ul(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<ul>``-Element (ungeordnete Liste).

    Args:
        *children: Kind-Elemente (``li``).
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``ul``.
    """
    return Element("ul", *children, **attrs)


def ol(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<ol>``-Element (geordnete Liste).

    Args:
        *children: Kind-Elemente (``li``).
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``ol``.
    """
    return Element("ol", *children, **attrs)


def li(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<li>``-Element (Listeneintrag).

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``li``.
    """
    return Element("li", *children, **attrs)


# ---------------------------------------------------------------------------
# Form
# ---------------------------------------------------------------------------


def form(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<form>``-Element.

    Args:
        *children: Kind-Elemente.
        **attrs: HTML-Attribute (z.B. ``action``, ``method``,
            ``hx_post``, ``hx_target``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``form``.
    """
    return Element("form", *children, **attrs)


def input(**attrs: object) -> Element:
    """Erzeugt ein ``<input>``-Element (Void-Element, kein schließender Tag).

    Args:
        **attrs: HTML-Attribute (z.B. ``type``, ``name``, ``value``,
            ``placeholder``, ``required``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``input``.
    """
    return Element("input", **attrs)


def label(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<label>``-Element.

    Args:
        *children: Kind-Elemente oder Texte.
        **attrs: HTML-Attribute (z.B. ``for_``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``label``.
    """
    return Element("label", *children, **attrs)


def textarea(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<textarea>``-Element.

    Args:
        *children: Textinhalt.
        **attrs: HTML-Attribute (z.B. ``name``, ``rows``, ``cols``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``textarea``.
    """
    return Element("textarea", *children, **attrs)


def select(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<select>``-Element (Dropdown).

    Args:
        *children: Kind-Elemente (``option``).
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``select``.
    """
    return Element("select", *children, **attrs)


def option(*children: Child, **attrs: object) -> Element:
    """Erzeugt ein ``<option>``-Element.

    Args:
        *children: Textinhalt.
        **attrs: HTML-Attribute (z.B. ``value``, ``selected``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``option``.
    """
    return Element("option", *children, **attrs)


# ---------------------------------------------------------------------------
# Media / Misc
# ---------------------------------------------------------------------------


def img(**attrs: object) -> Element:
    """Erzeugt ein ``<img>``-Element (Void-Element).

    Args:
        **attrs: HTML-Attribute (z.B. ``src``, ``alt``, ``width``, ``height``).

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``img``.
    """
    return Element("img", **attrs)


def br(**attrs: object) -> Element:
    """Erzeugt ein ``<br>``-Element (Zeilenumbruch, Void-Element).

    Args:
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``br``.
    """
    return Element("br", **attrs)


def hr(**attrs: object) -> Element:
    """Erzeugt ein ``<hr>``-Element (horizontale Linie, Void-Element).

    Args:
        **attrs: HTML-Attribute.

    Returns:
        Ein :class:`~htmlkit.core.element.Element` mit Tag ``hr``.
    """
    return Element("hr", **attrs)


__all__ = [
    # Text / Inline
    "a",
    "br",
    "em",
    "span",
    "strong",
    "p",
    # Block / Layout
    "article",
    "div",
    "footer",
    "header",
    "hr",
    "main",
    "nav",
    "section",
    # Headings
    "h1",
    "h2",
    "h3",
    # Interactive
    "button",
    # Table
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    # List
    "li",
    "ol",
    "ul",
    # Form
    "form",
    "img",
    "input",
    "label",
    "option",
    "select",
    "textarea",
]
