"""Badge-Komponente fuer kurze Statuskennzeichnungen."""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import span


class BadgeVariant(StrEnum):
    """Unterstuetzte Badge-Varianten."""

    DEFAULT = "default"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"
    INFO = "info"


class Badge(Component):
    """Rendert ein statisches Badge mit Variantenklasse."""

    text: str
    variant: BadgeVariant = BadgeVariant.DEFAULT
    extra_class: str = ""

    def render(self) -> Element:
        """Erstellt ein ``<span>`` mit Badge-CSS-Klassen."""
        base_class = f"badge badge--{self.variant.value}"
        final_class = f"{base_class} {self.extra_class}".strip()
        return span(self.text, cls=final_class)
