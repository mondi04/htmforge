"""HTML5 factory functions for htmlkit elements."""

from __future__ import annotations

from htmlkit.core.element import Child, Element

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

__all__ = [
    "a",
    "article",
    "aside",
    "blockquote",
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
    "header",
    "hr",
    "img",
    "input",
    "label",
    "li",
    "main",
    "nav",
    "ol",
    "option",
    "p",
    "pre",
    "section",
    "select",
    "span",
    "strong",
    "table",
    "tbody",
    "td",
    "textarea",
    "tfoot",
    "th",
    "thead",
    "tr",
    "ul",
]
