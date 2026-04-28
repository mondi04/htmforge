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

__all__ = ["Component", "Element"]

try:
    __version__ = _version("htmforge")
except PackageNotFoundError:
    __version__ = "0.0.0"
