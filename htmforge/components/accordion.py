"""Accordion mit details/summary-Elementen.

Example:
    >>> from htmforge.components import Accordion
    >>> Accordion(items=[("FAQ", "Answer text"), ("Info", "More text")]).to_html()
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import details, div, summary


class Accordion(Component):
    """Mehrere aufklappbare Abschnitte auf Basis von details/summary.

    Fields:
        items: list of (title, content) tuples
        open_index: int | None — index of initially open item, None = all closed
        item_cls: str — extra CSS class on each details element
    """

    items: list[tuple[str, str]]
    open_index: int | None = None
    item_cls: str = ""

    def render(self) -> Element:
        """Rendert das Accordion mit aufklappbaren Items."""
        accordion_items: list[Element] = []
        for i, (title, content) in enumerate(self.items):
            item_cls = f"accordion-item {self.item_cls}".strip()
            is_open = i == self.open_index
            accordion_items.append(
                details(
                    summary(title, cls="accordion-title"),
                    div(content, cls="accordion-content"),
                    cls=item_cls,
                    open=True if is_open else None,
                )
            )

        return div(*accordion_items, cls="accordion")
