"""Sucheingabe mit HTMX-Debounce.

Example:
    >>> from htmforge.components import SearchInput
    >>> s = SearchInput(name="q", search_url="/search", search_target="#results")
    >>> 'hx-trigger="keyup delay:300ms"' in s.to_html()
    True
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import div, input
from htmforge.htmx import hx_keyup_delay


class SearchInput(Component):
    """Text-Input mit automatischem hx-trigger keyup-Debounce.

    Renders: <div class="search-input-wrapper">
               <input type="search" name=name placeholder=placeholder
                      hx-get=search_url hx-trigger="keyup delay:{debounce_ms}ms"
                      hx-target=search_target [hx-indicator=indicator]>
             </div>

    Fields:
        name: str — input name attribute
        search_url: str — URL for hx-get (custom field, not Component.hx_get)
        search_target: str — CSS selector for swap target
            (custom field, not Component.hx_target)
        placeholder: str = "Suchen…"
        debounce_ms: int = 300
        indicator: str = "" — optional hx-indicator selector
    """

    name: str
    search_url: str
    search_target: str
    placeholder: str = "Suchen…"
    debounce_ms: int = 300
    indicator: str = ""

    def render(self) -> Element:
        """Erstellt den Such-Input mit Debounce und optionalem Indicator."""
        return div(
            input(
                type="search",
                name=self.name,
                placeholder=self.placeholder,
                hx_get=self.search_url,
                hx_trigger=hx_keyup_delay(self.debounce_ms),
                hx_target=self.search_target,
                hx_indicator=self.indicator or None,
            ),
            cls="search-input-wrapper",
        )
