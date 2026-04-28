"""Breadcrumb-Navigation.

Example:
    >>> from htmforge.components import Breadcrumb
    >>> bc = Breadcrumb(
    ...     items=[("Home", "/"), ("Produkte", "/produkte"), ("Detail", None)]
    ... )
    >>> bc.to_html()
    '<nav ...>...<span ...>Detail</span>...</nav>'
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import a, li, nav, ol, span


class Breadcrumb(Component):
    """Rendert eine Breadcrumb-Navigation als ``<nav>`` mit geordneter Liste.

    Items sind ``(label, url)``-Tupel.
    ``url=None`` markiert die aktuelle Seite und wird als ``<span>`` gerendert.

    Example:
        >>> Breadcrumb(items=[("Home", "/"), ("Aktuell", None)]).to_html()
        # contains <a href="/">Home</a> and <span ...>Aktuell</span>
    """

    items: list[tuple[str, str | None]]

    def render(self) -> Element:
        """Erstellt ``<nav>`` mit ``<ol>`` und ``<li>``-Eintraegen."""
        list_items: list[Element] = []
        last_index = len(self.items) - 1

        for index, (label, href) in enumerate(self.items):
            is_current = href is None or index == last_index
            if is_current:
                list_items.append(
                    li(
                        span(label, aria_current="page"),
                        cls="breadcrumb-item active",
                    )
                )
            else:
                list_items.append(
                    li(
                        a(label, href=href),
                        cls="breadcrumb-item",
                    )
                )

        return nav(ol(*list_items, cls="breadcrumb"), aria_label="breadcrumb")
