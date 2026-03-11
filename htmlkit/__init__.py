"""htmlkit — Typsichere, composable UI-Komponenten für Python.

Server-side rendered, framework-agnostisch, HTMX-first.

Quickstart::

    from htmlkit import Component
    from htmlkit.elements import div, p

    class Card(Component):
        title: str
        body: str

        def render(self):
            return div(p(self.title), p(self.body), cls="card")

    print(Card(title="Hello", body="World").to_html())
"""

from .core.component import Component
from .core.element import Element

__all__ = ["Component", "Element"]
__version__ = "0.1.0"
