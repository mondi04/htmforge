"""HTML5 factory functions for htmforge elements."""

from __future__ import annotations

from markupsafe import Markup

from htmforge.core.element import Child, Element


def raw(text: str) -> Markup:
    """Gibt einen String als rohes, nicht-escaptes HTML-Markup zurück.

    Verwende diese Funktion, um Inhalte von ``<script>`` oder ``<style>``-
    Tags einzubetten, die von markupsafe nicht erneut escaped werden sollen.

    Args:
        text: Der rohe Textinhalt (CSS, JavaScript …).

    Returns:
        Ein :class:`markupsafe.Markup`-Objekt.

    Example:
        >>> from htmforge.elements import script, raw
        >>> script(raw("console.log(1)")).to_html()
        '<script>console.log(1)</script>'
    """
    return Markup(text)  # noqa: S704

def div(*children: Child, **attrs: object) -> Element:
    """Block-Container."""
    return Element("div", *children, **attrs)

def span(*children: Child, **attrs: object) -> Element:
    """Inline-Container."""
    return Element("span", *children, **attrs)

def p(*children: Child, **attrs: object) -> Element:
    """Absatz-Element."""
    return Element("p", *children, **attrs)

def h1(*children: Child, **attrs: object) -> Element:
    """Ueberschrift Ebene 1."""
    return Element("h1", *children, **attrs)

def h2(*children: Child, **attrs: object) -> Element:
    """Ueberschrift Ebene 2."""
    return Element("h2", *children, **attrs)

def h3(*children: Child, **attrs: object) -> Element:
    """Ueberschrift Ebene 3."""
    return Element("h3", *children, **attrs)

def h4(*children: Child, **attrs: object) -> Element:
    """Ueberschrift Ebene 4."""
    return Element("h4", *children, **attrs)

def h5(*children: Child, **attrs: object) -> Element:
    """Ueberschrift Ebene 5."""
    return Element("h5", *children, **attrs)

def h6(*children: Child, **attrs: object) -> Element:
    """Ueberschrift Ebene 6."""
    return Element("h6", *children, **attrs)

def section(*children: Child, **attrs: object) -> Element:
    """Thematischer Abschnitt."""
    return Element("section", *children, **attrs)

def article(*children: Child, **attrs: object) -> Element:
    """Eigenstaendiger Inhalt."""
    return Element("article", *children, **attrs)

def main(*children: Child, **attrs: object) -> Element:
    """Hauptinhalt der Seite."""
    return Element("main", *children, **attrs)

def header(*children: Child, **attrs: object) -> Element:
    """Kopfbereich eines Abschnitts."""
    return Element("header", *children, **attrs)

def footer(*children: Child, **attrs: object) -> Element:
    """Fussbereich eines Abschnitts."""
    return Element("footer", *children, **attrs)

def nav(*children: Child, **attrs: object) -> Element:
    """Navigationsbereich."""
    return Element("nav", *children, **attrs)

def aside(*children: Child, **attrs: object) -> Element:
    """Nebeninhalt."""
    return Element("aside", *children, **attrs)

def ul(*children: Child, **attrs: object) -> Element:
    """Ungeordnete Liste."""
    return Element("ul", *children, **attrs)

def ol(*children: Child, **attrs: object) -> Element:
    """Geordnete Liste."""
    return Element("ol", *children, **attrs)

def li(*children: Child, **attrs: object) -> Element:
    """Listeneintrag."""
    return Element("li", *children, **attrs)

def table(*children: Child, **attrs: object) -> Element:
    """Tabellen-Container."""
    return Element("table", *children, **attrs)

def thead(*children: Child, **attrs: object) -> Element:
    """Tabellenkopf."""
    return Element("thead", *children, **attrs)

def tbody(*children: Child, **attrs: object) -> Element:
    """Tabelleninhalt."""
    return Element("tbody", *children, **attrs)

def tfoot(*children: Child, **attrs: object) -> Element:
    """Tabellenfuss."""
    return Element("tfoot", *children, **attrs)

def tr(*children: Child, **attrs: object) -> Element:
    """Tabellenzeile."""
    return Element("tr", *children, **attrs)

def th(*children: Child, **attrs: object) -> Element:
    """Tabellenkopf-Zelle."""
    return Element("th", *children, **attrs)

def td(*children: Child, **attrs: object) -> Element:
    """Tabellenzelle."""
    return Element("td", *children, **attrs)

def form(*children: Child, **attrs: object) -> Element:
    """Formular-Container."""
    return Element("form", *children, **attrs)

def input(**attrs: object) -> Element:
    """Eingabefeld als Void-Element."""
    return Element("input", **attrs)

def label(*children: Child, **attrs: object) -> Element:
    """Beschriftung fuer Formularfelder."""
    return Element("label", *children, **attrs)

def button(*children: Child, **attrs: object) -> Element:
    """Interaktiver Button."""
    return Element("button", *children, **attrs)

def select(*children: Child, **attrs: object) -> Element:
    """Auswahlliste."""
    return Element("select", *children, **attrs)

def option(*children: Child, **attrs: object) -> Element:
    """Eintrag in einer Auswahlliste."""
    return Element("option", *children, **attrs)

def textarea(*children: Child, **attrs: object) -> Element:
    """Mehrzeiliges Texteingabefeld."""
    return Element("textarea", *children, **attrs)

def a(*children: Child, **attrs: object) -> Element:
    """Hyperlink-Element."""
    return Element("a", *children, **attrs)

def img(**attrs: object) -> Element:
    """Bild als Void-Element."""
    return Element("img", **attrs)

def figure(*children: Child, **attrs: object) -> Element:
    """Container fuer Medieninhalte."""
    return Element("figure", *children, **attrs)

def figcaption(*children: Child, **attrs: object) -> Element:
    """Bildunterschrift fuer figure."""
    return Element("figcaption", *children, **attrs)

def hr(**attrs: object) -> Element:
    """Thematischer Trennstrich als Void-Element."""
    return Element("hr", **attrs)

def br(**attrs: object) -> Element:
    """Zeilenumbruch als Void-Element."""
    return Element("br", **attrs)

def strong(*children: Child, **attrs: object) -> Element:
    """Wichtiger, stark hervorgehobener Text."""
    return Element("strong", *children, **attrs)

def em(*children: Child, **attrs: object) -> Element:
    """Betonter Text."""
    return Element("em", *children, **attrs)

def code(*children: Child, **attrs: object) -> Element:
    """Inline-Codefragment."""
    return Element("code", *children, **attrs)

def pre(*children: Child, **attrs: object) -> Element:
    """Vorformatierter Textblock."""
    return Element("pre", *children, **attrs)

def blockquote(*children: Child, **attrs: object) -> Element:
    """Blockzitat."""
    return Element("blockquote", *children, **attrs)


# ---------------------------------------------------------------------------
# Document structure
# ---------------------------------------------------------------------------

def html(*children: Child, **attrs: object) -> Element:
    """Wurzelelement des HTML-Dokuments."""
    return Element("html", *children, **attrs)


def head(*children: Child, **attrs: object) -> Element:
    """Dokumentkopf mit Metadaten."""
    return Element("head", *children, **attrs)


def body(*children: Child, **attrs: object) -> Element:
    """Sichtbarer Dokumentinhalt."""
    return Element("body", *children, **attrs)


def title(*children: Child, **attrs: object) -> Element:
    """Dokumenttitel (im Browser-Tab)."""
    return Element("title", *children, **attrs)


def meta(**attrs: object) -> Element:
    """Metadaten-Void-Element."""
    return Element("meta", **attrs)


def link(**attrs: object) -> Element:
    """Externe Ressource als Void-Element (z.B. Stylesheet)."""
    return Element("link", **attrs)


def script(*children: Child, **attrs: object) -> Element:
    """Skript-Block oder externes Skript.

    Verwende :func:`raw` für Inline-JavaScript, damit der Inhalt
    nicht escaped wird.
    """
    return Element("script", *children, **attrs)


def style(*children: Child, **attrs: object) -> Element:
    """Inline-CSS-Block.

    Verwende :func:`raw` für CSS-Inhalt, damit er nicht escaped wird.
    """
    return Element("style", *children, **attrs)


def noscript(*children: Child, **attrs: object) -> Element:
    """Fallback-Inhalt wenn JavaScript deaktiviert ist."""
    return Element("noscript", *children, **attrs)

__all__ = [
    "a",
    "article",
    "aside",
    "blockquote",
    "body",
    "br",
    "button",
    "code",
    "div",
    "em",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hr",
    "html",
    "img",
    "input",
    "label",
    "li",
    "link",
    "main",
    "meta",
    "nav",
    "noscript",
    "ol",
    "option",
    "p",
    "pre",
    "raw",
    "script",
    "section",
    "select",
    "span",
    "strong",
    "style",
    "table",
    "tbody",
    "td",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "title",
    "tr",
    "ul",
]
