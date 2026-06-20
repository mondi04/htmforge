"""Dropdown-Menü mit Trigger-Button und HTMX-Toggle.

Example:
    >>> from htmforge.components import Dropdown
    >>> Dropdown(
    ...     label="Actions",
    ...     items=[("Edit", "/edit"), ("Delete", "/delete")],
    ... ).to_html()
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import a, button, div
from htmforge.htmx import HxSwap


class Dropdown(Component):
    """Trigger-Button mit verstecktem Menü, HTMX-togglebar.

    Renders:
        div(cls="dropdown")
          button(label, hx_get=toggle_url, hx_target="#dropdown_id-menu",
                 hx_swap=HxSwap.OUTER_HTML, cls="dropdown-trigger")
          div(id=f"{dropdown_id}-menu", cls="dropdown-menu")
            For each (label, url):
              a(label, href=url, cls="dropdown-item")

    Fields:
        label: str — trigger button label
        items: list of (label, url) tuples
        dropdown_id: str — unique HTML id prefix, default "dropdown"
        toggle_url: str — HTMX URL to reload/toggle menu, default ""
    """

    label: str
    items: list[tuple[str, str]]
    dropdown_id: str = "dropdown"
    toggle_url: str = ""

    def render(self) -> Element:
        """Rendert das Dropdown-Menü mit Trigger-Button."""
        menu_id = f"{self.dropdown_id}-menu"

        # Trigger-Button mit optionalen HTMX-Attributen
        button_attrs: dict[str, object] = {"cls": "dropdown-trigger"}
        if self.toggle_url:
            button_attrs["hx_get"] = self.toggle_url
            button_attrs["hx_target"] = f"#{menu_id}"
            button_attrs["hx_swap"] = HxSwap.OUTER_HTML

        trigger_button = button(self.label, **button_attrs)

        # Menü-Items
        menu_items: list[Element] = []
        for item_label, url in self.items:
            menu_items.append(a(item_label, href=url, cls="dropdown-item"))

        # Menü-Div
        menu_div = div(*menu_items, id=menu_id, cls="dropdown-menu")

        # Root-Div
        return div(trigger_button, menu_div, cls=merge_cls("dropdown", self.extra_cls))
    