"""Component-Level Asset-Injection: CSS/JS-Sammlung fuer Component-Baeume (#3).

Components koennen ueber die ClassVars ``css_files``/``js_files`` (siehe
:class:`~htmforge.core.component.Component`) ihre eigenen Asset-Abhaengigkeiten
deklarieren. :func:`collect_assets` durchlaeuft einen Element/Component-Baum
und sammelt alle referenzierten Dateien dedupliziert in Deklarationsreihenfolge
— unabhaengig davon, wie oft eine Komponente (bzw. ihr Typ) im Baum vorkommt.

Example:
    >>> from htmforge import Component
    >>> from htmforge.core.assets import collect_assets
    >>> from htmforge.core.element import Element
    >>> from htmforge.elements import div
    >>>
    >>> class Chart(Component):
    ...     css_files = ["chart.css"]
    ...     js_files = ["chart.js"]
    ...     def render(self) -> Element:
    ...         return div(cls="chart")
    ...
    >>> collect_assets(div(Chart(), Chart()))
    (['chart.css'], ['chart.js'])
"""

from __future__ import annotations

from htmforge.core.component import Component
from htmforge.core.element import Element

Node = "Element | Component | str | None"


def collect_assets(
    *nodes: Element | Component | str | None,
) -> tuple[list[str], list[str]]:
    """Sammelt alle ``css_files``/``js_files`` aus einem Element/Component-Baum.

    Durchlaeuft rekursiv sowohl bereits verschachtelte ``Element``-Kinder als
    auch noch nicht gerenderte ``Component``-Instanzen (ueber ``render()``),
    damit Assets unabhaengig davon gefunden werden, auf welcher Ebene eine
    Component im Baum steht.

    Args:
        *nodes: Beliebig viele Wurzel-Knoten (typischerweise die Kinder
            einer Seite).

    Returns:
        Ein Tupel ``(css_files, js_files)`` — jeweils dedupliziert in der
        Reihenfolge des ersten Auftretens.
    """
    css: list[str] = []
    js: list[str] = []
    seen_css: set[str] = set()
    seen_js: set[str] = set()

    def _extend(target: list[str], seen: set[str], values: list[str]) -> None:
        for value in values:
            if value not in seen:
                seen.add(value)
                target.append(value)

    def _walk(node: Element | Component | str | None) -> None:
        if node is None or isinstance(node, str):
            return
        if isinstance(node, Component):
            _extend(css, seen_css, type(node).css_files)
            _extend(js, seen_js, type(node).js_files)
            _walk(node.render())
            return
        if isinstance(node, Element):
            for child in node._children:  # noqa: SLF001
                _walk(child)

    for node in nodes:
        _walk(node)

    return css, js


__all__ = ["collect_assets"]
