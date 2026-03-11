"""HTML-Primitive Basisklasse für htmlkit.

Stellt die ``Element``-Klasse bereit, die einen einzelnen HTML-Tag
repräsentiert und via :meth:`Element.to_html` in einen sicheren
HTML-String gerendert werden kann.
"""

from __future__ import annotations

from typing import Union

from markupsafe import Markup, escape

# Ein Kind-Element ist entweder ein weiteres Element, ein Rohstring oder None.
Child = Union["Element", str, None]

# Void-Elemente dürfen keine schließenden Tags haben (HTML5-Spec).
_VOID_ELEMENTS: frozenset[str] = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)


class Element:
    """Repräsentiert einen einzelnen HTML-Tag mit Kindern und Attributen.

    Args:
        tag: Der HTML-Tag-Name (z.B. ``"div"``, ``"span"``).
        *children: Beliebig viele Kind-Elemente (``Element``, ``str`` oder
            ``None``). ``None``-Werte werden stillschweigend ignoriert.
        **attrs: HTML-Attribute als Keyword-Argumente.

    Attribute-Konventionen:
        - ``cls`` wird zu ``class`` im HTML.
        - ``for_`` wird zu ``for`` im HTML.
        - Unterstriche innerhalb von Attribut-Namen werden zu Bindestrichen
          konvertiert (``hx_get`` → ``hx-get``, ``data_id`` → ``data-id``).
        - Boolesche Attribute (``True``) werden als eigenständige Flags
          gerendert (``disabled``, ``checked`` ...).
        - Attribute mit Wert ``False`` oder ``None`` werden weggelassen.

    Example:
        >>> el = Element("div", Element("span", "Hallo"), cls="container")
        >>> el.to_html()
        '<div class="container"><span>Hallo</span></div>'
    """

    __slots__ = ("_attrs", "_children", "_tag")

    def __init__(self, tag: str, *children: Child, **attrs: object) -> None:
        """Initialisiert ein Element mit Tag-Name, Kindern und Attributen."""
        self._tag: str = tag.lower()
        self._children: tuple[Child, ...] = children
        self._attrs: dict[str, object] = attrs

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def to_html(self) -> str:
        """Rendert das Element rekursiv zu einem sicheren HTML-String.

        Alle Text-Inhalte werden durch ``markupsafe.escape`` gesichert, damit
        kein unbeabsichtigtes HTML injiziert werden kann.

        Returns:
            Ein vollständiger, wohlgeformter HTML-String.
        """
        attrs_str = self._render_attrs()
        tag = self._tag

        if tag in _VOID_ELEMENTS:
            return f"<{tag}{attrs_str}>"

        inner = self._render_children()
        return f"<{tag}{attrs_str}>{inner}</{tag}>"

    def __repr__(self) -> str:
        """Gibt eine kurze Debug-Darstellung zurück."""
        return f"Element(tag={self._tag!r}, attrs={self._attrs!r})"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _render_attrs(self) -> str:
        """Konvertiert das Attribut-Dict in einen HTML-Attribut-String.

        Returns:
            Ein String der Form `` key="value" key2`` (mit führendem
            Leerzeichen, wenn Attribute vorhanden sind).
        """
        parts: list[str] = []

        for raw_key, value in self._attrs.items():
            if value is None or value is False:
                continue

            html_key = _normalize_attr_name(raw_key)

            if value is True:
                # Boolesches Attribut: nur Flag, kein Wert
                parts.append(html_key)
            else:
                safe_value = escape(str(value))
                parts.append(f'{html_key}="{safe_value}"')

        if not parts:
            return ""
        return " " + " ".join(parts)

    def _render_children(self) -> str:
        """Rendert alle Kind-Elemente zu einem zusammengesetzten HTML-String.

        Returns:
            Der verkettete HTML-String aller Kinder.
        """
        chunks: list[str] = []
        for child in self._children:
            if child is None:
                continue
            if isinstance(child, Element):
                chunks.append(child.to_html())
            else:
                # Roher String → escapen, damit kein XSS möglich ist
                chunks.append(str(escape(child)))
        return "".join(chunks)


def _normalize_attr_name(name: str) -> str:
    """Normalisiert einen Python-Attribut-Namen zu einem HTML-Attribut-Namen.

    Konvertierungsregeln (in Reihenfolge):
        1. ``cls``  → ``class``
        2. ``for_`` → ``for``
        3. Führende/nachfolgende Unterstriche werden entfernt.
        4. Unterstriche innerhalb des Namens werden zu Bindestrichen
           (``hx_get`` → ``hx-get``, ``data_foo_bar`` → ``data-foo-bar``).

    Args:
        name: Der Python-seitige Attribut-Name.

    Returns:
        Der fertige HTML-Attribut-Name als Kleinbuchstaben-String.

    Example:
        >>> _normalize_attr_name("cls")
        'class'
        >>> _normalize_attr_name("hx_get")
        'hx-get'
        >>> _normalize_attr_name("for_")
        'for'
    """
    if name == "cls":
        return "class"
    # Entferne umgebende Unterstriche (z.B. for_ → for)
    name = name.strip("_")
    # Unterstriche → Bindestriche
    return name.replace("_", "-")
