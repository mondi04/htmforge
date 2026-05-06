"""Toast-Benachrichtigung, HTMX OOB-swap kompatibel.

Example:
    >>> from htmforge.components import Toast, ToastVariant
    >>> Toast(message="Gespeichert", variant=ToastVariant.SUCCESS).to_html()
    '<div id="toast" class="toast toast-success" ...>Gespeichert</div>'
"""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import div


class ToastVariant(StrEnum):
    """Verfügbare Toast-Varianten."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Toast(Component):
    """Timed notification box, HTMX OOB-swap kompatibel.

    Renders a div with id=toast_id for HTMX out-of-band swapping.
    Use hx-swap-oob="true" in HTMX responses to inject toasts.

    Fields:
        message: str — notification text
        variant: ToastVariant — visual style
        toast_id: str — HTML id, default "toast"
        duration_ms: int — auto-dismiss after ms via JS, 0 = no auto-dismiss
    """

    message: str
    variant: ToastVariant = ToastVariant.INFO
    toast_id: str = "toast"
    duration_ms: int = 3000

    def render(self) -> Element:
        """Rendert die Toast-Benachrichtigung mit OOB-Swap-Support."""
        attrs: dict[str, object] = {
            "id": self.toast_id,
            "cls": f"toast toast-{self.variant.value}",
            "hx_swap_oob": "true",
        }
        if self.duration_ms > 0:
            attrs["data_duration"] = str(self.duration_ms)

        return div(self.message, **attrs)
