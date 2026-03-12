"""Tabellen-Komponente fuer strukturierte Daten.

Example:
    >>> from htmforge.components import DataTable
    >>> table = DataTable(headers=["Name"], rows=[["Ada"]])
    >>> table.to_html()
    '<table><thead><tr><th>Name</th></tr></thead><tbody><tr><td>Ada</td></tr></tbody></table>'
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import table, tbody, td, th, thead, tr
from htmforge.htmx import HxTrigger


class DataTable(Component):
    """Rendert eine einfache Datentabelle mit optionalem HTMX-Reload."""

    headers: list[str]
    rows: list[list[str]]
    hx_url: str | None = None
    empty_message: str = "Keine Einträge"

    def render(self) -> Element:
        """Erstellt ``<table>`` mit ``<thead>`` und ``<tbody>``."""
        header_row = tr(*(th(header) for header in self.headers))

        body_rows: list[Element]
        if self.rows:
            body_rows = [tr(*(td(cell) for cell in row)) for row in self.rows]
        else:
            colspan = max(len(self.headers), 1)
            body_rows = [tr(td(self.empty_message, colspan=colspan))]

        attrs: dict[str, object] = {}
        if self.hx_url is not None:
            attrs["hx_get"] = self.hx_url
            attrs["hx_trigger"] = HxTrigger.LOAD

        return table(
            thead(header_row),
            tbody(*body_rows),
            **attrs,
        )
