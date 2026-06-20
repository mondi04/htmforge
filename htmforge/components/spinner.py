"""Spinner-Komponente fuer Ladeanimationen.

Example:
    >>> from htmforge.components import Spinner, SpinnerSize
    >>> Spinner(size=SpinnerSize.MD).to_html()
    '<div class="spinner spinner-md" role="status" aria-label="Loading"></div>'
"""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import div


class SpinnerSize(StrEnum):
    """Verfügbare Spinner-Größen."""

    SM = "sm"
    MD = "md"
    LG = "lg"


class Spinner(Component):
    """Barrierefreier Ladeindikator mit Groessenvarianten.

    Example:
        >>> Spinner().to_html()
        '<div class="spinner spinner-md" role="status" aria-label="Loading"></div>'
    """

    size: SpinnerSize = SpinnerSize.MD
    label: str = "Loading"

    def render(self) -> Element:
        """Rendert den Spinner mit Größenklasse und Accessibility-Attributen."""
        return div(
            cls=merge_cls(f"spinner spinner-{self.size.value}", self.extra_cls),
            role="status",
            aria_label=self.label,
        )
