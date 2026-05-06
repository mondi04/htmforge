"""Tabellen-Komponente fuer strukturierte Daten.

Example:
    >>> from htmforge.components import DataTable
    >>> table = DataTable(headers=["Name"], rows=[["Ada"]])
    >>> table.to_html()
    '<table><thead><tr><th>Name</th></tr></thead><tbody><tr><td>Ada</td></tr></tbody></table>'
"""

from __future__ import annotations

from pydantic import BaseModel

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import a, div, table, tbody, td, th, thead, tr
from htmforge.htmx import HxTrigger


class ColumnDef(BaseModel):
    """Spaltenkonfiguration fuer DataTable.

    Fields:
        key: Schlüssel für dict_rows oder Index-Position
        label: Angezeigter Spaltenname (default = key)
        sortable: Ob die Spalte klickbar/sortierbar ist
        width: Optionale CSS-Breite z.B. "120px" oder "10%"
    """

    key: str
    label: str = ""
    sortable: bool = False
    width: str = ""

    @property
    def display_label(self) -> str:
        """Gibt label zurück, falls gesetzt, sonst key."""
        return self.label or self.key


class DataTable(Component):
    """Rendert eine einfache Datentabelle mit optionalem HTMX-Reload."""

    headers: list[str] = []
    rows: list[list[str]] = []
    dict_rows: list[dict[str, str]] | None = None
    columns: list[ColumnDef] | None = None
    hx_url: str | None = None
    sort_url: str = ""
    current_sort: str = ""
    sort_dir: str = "asc"
    empty_message: str = "Keine Einträge"

    def render(self) -> Element:
        """Erstellt ``div.table-wrapper > table.table`` mit ``thead``/``tbody``."""
        # Build header row
        header_row = self._render_header_row()

        # Build body rows
        body_rows = self._render_body_rows()

        attrs: dict[str, object] = {}
        if self.hx_url is not None:
            attrs["hx_get"] = self.hx_url
            attrs["hx_trigger"] = HxTrigger.LOAD

        return div(
            table(
                thead(header_row),
                tbody(*body_rows),
                cls="table",
                **attrs,
            ),
            cls="table-wrapper",
        )

    def _render_header_row(self) -> Element:
        """Rendert die Header-Zeile mit optional sortierbaren Spalten."""
        if self.columns is not None:
            # Use ColumnDef
            header_cells = []
            for col in self.columns:
                if col.sortable and self.sort_url:
                    # Sortierbar: render as link
                    next_dir = (
                        "desc"
                        if self.current_sort == col.key and self.sort_dir == "asc"
                        else "asc"
                    )
                    link = a(
                        col.display_label,
                        href="#",
                        hx_get=f"{self.sort_url}?sort={col.key}&dir={next_dir}",
                        hx_target="this",
                        cls="sort-link",
                    )
                    style_attr = col.width if col.width else None
                    header_cells.append(th(link, style=style_attr, cls="sortable"))
                else:
                    # Nicht sortierbar oder kein sort_url
                    style_attr = col.width if col.width else None
                    header_cells.append(th(col.display_label, style=style_attr))
            return tr(*header_cells)
        else:
            # Use headers list
            return tr(*(th(header) for header in self.headers))

    def _render_body_rows(self) -> list[Element]:
        """Rendert die Body-Zeilen."""
        # Use dict_rows if provided
        if self.dict_rows is not None:
            if not self.dict_rows:
                # Empty dict_rows: show empty message
                if self.columns is not None:
                    colspan = max(len(self.columns), 1)
                else:
                    colspan = max(len(self.headers), 1)
                return [tr(td(self.empty_message, colspan=colspan, cls="table__empty"))]

            # Render dict rows
            body_rows = []
            for row_dict in self.dict_rows:
                if self.columns is not None:
                    # Use ColumnDef keys
                    cells = [row_dict.get(col.key, "") for col in self.columns]
                else:
                    # Use headers as keys
                    cells = [row_dict.get(h, "") for h in self.headers]
                body_rows.append(tr(*(td(cell) for cell in cells)))
            return body_rows

        # Use rows: list[list[str]]
        if self.rows:
            return [tr(*(td(cell) for cell in row)) for row in self.rows]

        # Both empty: show empty message
        colspan = max(len(self.headers), 1)
        return [tr(td(self.empty_message, colspan=colspan, cls="table__empty"))]
