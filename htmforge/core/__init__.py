"""Core-Paket von htmforge.

Enthält die primitiven Basis-Klassen :class:`~htmforge.core.element.Element`
und :class:`~htmforge.core.component.Component`.
"""

from .component import Component
from .element import Element

__all__ = ["Component", "Element"]
