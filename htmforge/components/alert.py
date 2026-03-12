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
    close_label: str = "Schließen"

    def render(self) -> Element:
        """Erstellt ein ``<div>`` mit Variantenklasse und optionalem Schliessen."""
        children: list[Element | str] = [self.message]
        if self.dismissible:
            children.append(
                button(
                    "×",
                    type="button",
                    class_="alert__close",
                    aria_label=self.close_label,
                    onclick="this.closest('.alert').remove()",
                )
            )
        return div(*children, cls=f"alert alert-{self.variant.value}")
