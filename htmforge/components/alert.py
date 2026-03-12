"""Alert-Komponente fuer Statusmeldungen.

Example:
    >>> from htmforge.components import Alert, AlertVariant
    >>> Alert(message="Gespeichert", variant=AlertVariant.SUCCESS).to_html()
    '<div class="alert alert-success">Gespeichert</div>'
"""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import button, div
from htmforge.htmx import HxSwap, HxTarget


class AlertVariant(StrEnum):
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
                # TODO: replace with JS-based dismiss
                # (hx_get="" triggers GET on current URL)
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
