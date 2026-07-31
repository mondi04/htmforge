"""Grid-basierte Dashboard-Layout-Komponente fuer htmforge.

Example:
    >>> from htmforge.components import DashboardLayout, Widget
    >>> from htmforge.elements import p
    >>> dashboard = DashboardLayout(
    ...     widgets=[
    ...         Widget(title="Sales", content=p("$12,400"), col_span=4),
    ...         Widget(title="Recent Orders", content=p("..."), col_span=8),
    ...     ]
    ... )
    >>> "dashboard-widget" in dashboard.to_html()
    True
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import div, h3


class Widget(BaseModel):
    """Eine einzelne Dashboard-Kachel: Titel + beliebiger Inhalt in einer Grid-Zelle.

    Fields:
        title: str — Ueberschrift der Kachel, leer = kein Titel gerendert
        content: Element | Component — der eigentliche Widget-Inhalt
        col_span: int — Anzahl belegter Grid-Spalten (relativ zu
            ``DashboardLayout.columns``), default 12 (volle Breite)
        widget_cls: str — zusaetzliche CSS-Klasse auf der Kachel
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    title: str = ""
    content: Element | Component
    col_span: int = 12
    widget_cls: str = ""


class DashboardLayout(Component):
    """Rendert ``Widget``-Instanzen als CSS-Grid mit konfigurierbaren Spalten.

    Jedes ``Widget`` belegt ``col_span`` von ``columns`` Grid-Spalten (per
    ``style="grid-column: span N"``), damit sich Layouts wie ein 4/8- oder
    12/12-Split deklarativ statt durch manuelles div/row/col-Verschachteln
    beschreiben lassen.

    Fields:
        widgets: list[Widget] — die zu rendernden Kacheln, in Reihenfolge
        columns: int — Gesamtzahl der Grid-Spalten, default 12
        gap: str — CSS-``gap``-Wert zwischen Kacheln, default "1rem"
    """

    widgets: list[Widget] = []
    columns: int = 12
    gap: str = "1rem"

    def render(self) -> Element:
        """Erstellt ``div.dashboard`` mit einer Kachel pro ``Widget``."""
        widget_els: list[Element] = []
        for widget in self.widgets:
            children: list[Element] = []
            if widget.title:
                children.append(h3(widget.title, cls="dashboard-widget-title"))
            children.append(div(widget.content, cls="dashboard-widget-body"))
            widget_els.append(
                div(
                    *children,
                    cls=merge_cls("dashboard-widget", widget.widget_cls),
                    style=f"grid-column: span {widget.col_span}",
                )
            )

        style = (
            f"display: grid; "
            f"grid-template-columns: repeat({self.columns}, 1fr); "
            f"gap: {self.gap}"
        )
        return div(*widget_els, cls=merge_cls("dashboard", self.extra_cls), style=style)
