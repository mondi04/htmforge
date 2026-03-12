"""Breadcrumb-Komponente fuer hierarchische Navigation."""

from __future__ import annotations

from pydantic import BaseModel

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import a, li, nav, ol, span


class BreadcrumbItem(BaseModel):
    """Ein einzelnes Breadcrumb-Element."""

    label: str
    href: str | None = None


class Breadcrumb(Component):
    """Rendert eine Breadcrumb-Navigation mit optionalen Links."""

    items: list[BreadcrumbItem]
    separator: str = "/"

    def render(self) -> Element:
        """Erstellt ``<nav>`` und optional eine ``<ol>`` mit Trennzeichen."""
        if not self.items:
            return nav(cls="breadcrumb", aria_label="breadcrumb")

        list_children: list[Element] = []
        last_index = len(self.items) - 1

        for index, item in enumerate(self.items):
            is_active = index == last_index or item.href is None

            if is_active:
                list_children.append(
                    li(
                        item.label,
                        cls="breadcrumb__item breadcrumb__item--active",
                        aria_current="page",
                    )
                )
            else:
                list_children.append(
                    li(
                        a(item.label, href=item.href, cls="breadcrumb__link"),
                        cls="breadcrumb__item",
                    )
                )

            if index < last_index:
                list_children.append(span(self.separator, cls="breadcrumb__separator"))

        return nav(
            ol(*list_children, cls="breadcrumb__list"),
            cls="breadcrumb",
            aria_label="breadcrumb",
        )
