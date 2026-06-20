"""Tab-Navigation mit HTMX lazy-load pro Tab.

Example:
    >>> from htmforge.components import Tabs
    >>> tabs = Tabs(
    ...     tabs=[("Overview", "/tabs/overview"), ("Details", "/tabs/details")],
    ...     active=0,
    ...     target="#tab-panel",
    ... )
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import button, div
from htmforge.htmx import HxSwap


class Tabs(Component):
    """Rendert eine Tab-Leiste. Jeder Tab laedt seinen Inhalt via HTMX.

    Fields:
        tabs: list of (label, hx_url) tuples
        active: index of the active tab (0-based)
        target: CSS selector for the content panel to swap into
        tab_cls: extra CSS class on the tab bar wrapper div
    """

    tabs: list[tuple[str, str]]
    active: int = 0
    target: str = "#tab-panel"
    tab_cls: str = ""

    def render(self) -> Element:
        """Rendert die Tab-Leiste mit aktiven/inaktiven Tabs."""
        tab_buttons: list[Element] = []
        for i, (label, url) in enumerate(self.tabs):
            if i == self.active:
                # Aktiver Tab: disabled, keine HTMX-Attribute
                tab_buttons.append(
                    button(
                        label,
                        cls="tab tab-active",
                        disabled=True,
                    )
                )
            else:
                # Inaktiver Tab: mit HTMX-Attributen
                tab_buttons.append(
                    button(
                        label,
                        cls="tab",
                        hx_get=url,
                        hx_target=self.target,
                        hx_swap=HxSwap.INNER_HTML,
                    )
                )

        tab_cls = merge_cls("tabs", self.tab_cls, self.extra_cls)
        return div(*tab_buttons, cls=tab_cls)
