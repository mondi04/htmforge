"""Spinner-Komponente fuer Ladezustandsanzeige."""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import div, span


class SpinnerSize(StrEnum):
    """Verfuegbare Groessen fuer den Spinner."""

    SMALL = "sm"
    MEDIUM = "md"
    LARGE = "lg"


class Spinner(Component):
    """Rendert einen barrierearmen Ladeindikator."""

    size: SpinnerSize = SpinnerSize.MEDIUM
    label: str = "Laden..."

    def render(self) -> Element:
        """Erstellt ``div.spinner`` mit Screen-Reader-Text."""
        return div(
            span(self.label, cls="spinner__sr-only"),
            cls=f"spinner spinner--{self.size.value}",
            role="status",
            aria_label=self.label,
        )
