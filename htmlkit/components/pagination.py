"""Pagination-Komponente fuer seitenweises Laden mit HTMX.

Example:
    >>> from htmlkit.components import Pagination
    >>> pager = Pagination(current_page=2, total_pages=3, hx_url="/users?page={page}", hx_target="#users")
    >>> "hx-get=\"/users?page=1\"" in pager.to_html()
    True
"""

from __future__ import annotations

from htmlkit import Component
from htmlkit.core.element import Element
from htmlkit.elements import a, li, ul


class Pagination(Component):
    """Rendert Previous/Next und Seitenlinks fuer HTMX-Navigation."""

    current_page: int
    total_pages: int
    hx_url: str
    hx_target: str

    def render(self) -> Element:
        """Erstellt eine ``<ul>`` mit Seitenlinks inklusive Previous/Next."""
        items: list[Element] = [self._previous_link()]

        for page in range(1, self.total_pages + 1):
            if page == self.current_page:
                items.append(li(a(str(page), href="#"), cls="active"))
            else:
                items.append(
                    li(
                        a(
                            str(page),
                            href="#",
                            hx_get=self.hx_url.format(page=page),
                            hx_target=self.hx_target,
                        )
                    )
                )

        items.append(self._next_link())
        return ul(*items, cls="pagination")

    def _previous_link(self) -> Element:
        """Rendert den Previous-Link mit deaktiviertem Zustand auf Seite 1."""
        if self.current_page <= 1:
            return li(a("Previous", href="#"), cls="disabled")
        prev_page = self.current_page - 1
        return li(
            a(
                "Previous",
                href="#",
                hx_get=self.hx_url.format(page=prev_page),
                hx_target=self.hx_target,
            )
        )

    def _next_link(self) -> Element:
        """Rendert den Next-Link mit deaktiviertem Zustand auf letzter Seite."""
        if self.current_page >= self.total_pages:
            return li(a("Next", href="#"), cls="disabled")
        next_page = self.current_page + 1
        return li(
            a(
                "Next",
                href="#",
                hx_get=self.hx_url.format(page=next_page),
                hx_target=self.hx_target,
            )
        )
