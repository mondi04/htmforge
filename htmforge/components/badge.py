"""Badge-Komponente fuer kleine Inline-Labels.

Example:
    >>> from htmforge.components import Badge, BadgeVariant
    >>> Badge(text="Neu", variant=BadgeVariant.SUCCESS).to_html()
    '<span class="badge badge-success">Neu</span>'
"""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import span


class BadgeVariant(StrEnum):
    """Unterstuetzte Badge-Varianten."""

    DEFAULT = "default"
    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"


class Badge(Component):
    """Rendert ein kleines Inline-Label mit Variantenklasse.

    Example:
        >>> Badge(text="3", variant=BadgeVariant.DANGER).to_html()
        '<span class="badge badge-danger">3</span>'
    """

    text: str
    variant: BadgeVariant = BadgeVariant.DEFAULT

    def render(self) -> Element:
        """Erstellt ein ``<span>`` mit Variantenklasse."""
        return span(self.text, cls=f"badge badge-{self.variant.value}")
