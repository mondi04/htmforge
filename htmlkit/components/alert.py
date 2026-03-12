"""Alert-Komponente fuer Statusmeldungen.

Example:
    >>> from htmlkit.components import Alert, AlertVariant
    >>> Alert(message="Gespeichert", variant=AlertVariant.SUCCESS).to_html()
    '<div class="alert alert-success">Gespeichert</div>'
"""

from __future__ import annotations

from enum import Enum

from htmlkit import Component
from htmlkit.core.element import Element
from htmlkit.elements import button, div
from htmlkit.htmx import HxSwap, HxTarget


class AlertVariant(str, Enum):
    """Unterstuetzte Alert-Varianten."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Alert(Component):
    """Rendert eine Alert-Box mit optionalem Dismiss-Button."""

    message: str
    variant: AlertVariant = AlertVariant.INFO
    dismissible: bool = False

    def render(self) -> Element:
        """Erstellt ein ``<div>`` mit Variantenklasse und optionalem Schliessen."""
        children: list[Element | str] = [self.message]
        if self.dismissible:
            children.append(
                button(
                    "×",
                    type="button",
                    hx_get="",
                    hx_target=HxTarget.CLOSEST_DIV,
                    hx_swap=HxSwap.DELETE,
                    cls="alert-close",
                )
            )
        return div(*children, cls=f"alert alert-{self.variant.value}")
