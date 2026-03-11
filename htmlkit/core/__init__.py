"""Core-Paket von htmlkit.

Enthält die primitiven Basis-Klassen :class:`~htmlkit.core.element.Element`
und :class:`~htmlkit.core.component.Component`.
"""

from .component import Component
from .element import Element

__all__ = ["Component", "Element"]
