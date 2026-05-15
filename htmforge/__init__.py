"""htmforge — Typsichere, composable UI-Komponenten für Python.

Server-side rendered, framework-agnostisch, HTMX-first.

Quickstart::

    from htmforge import Component
    from htmforge.elements import div, p

    class Card(Component):
        title: str
        body: str

        def render(self):
            return div(p(self.title), p(self.body), cls="card")

    print(Card(title="Hello", body="World").to_html())
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

from .core.component import Component
from .core.element import Element


def render(component: "Component | Element") -> str:
    """Top-level Convenience-Funktion zum Rendern von Komponenten und Elementen.

    Args:
        component: Eine Component- oder Element-Instanz.

    Returns:
        Den gerenderten HTML-String.

    Example:
        >>> from htmforge import render
        >>> from htmforge.elements import div
        >>> render(div("Hello"))
        '<div>Hello</div>'
    """
    return component.to_html()


def when(
    condition: bool,
    element: "Element | Component",
) -> "Element | Component | None":
    """Gibt das Element zurueck wenn condition True ist, sonst None.

    Nützlich fuer bedingte Renders in render()-Methoden ohne if-Ausdrücke.

    Args:
        condition: Wenn True wird das Element zurueckgegeben.
        element: Das zu rendernde Element oder die Komponente.

    Returns:
        Das Element wenn condition True, sonst None.

    Example:
        >>> from htmforge import when
        >>> from htmforge.elements import div, span
        >>> div(when(True, span("visible")), when(False, span("hidden")))
        # renders: <div><span>visible</span></div>
    """
    return element if condition else None


__all__ = ["Component", "Element", "render", "when"]

try:
    __version__ = _version("htmforge")
except PackageNotFoundError:
    __version__ = "0.3.3"
