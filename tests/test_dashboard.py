"""Tests fuer die ``DashboardLayout``- und ``Widget``-Komponenten (#24)."""

from __future__ import annotations

from htmforge.components import Badge, DashboardLayout, Widget
from htmforge.elements import p


class TestWidget:
    """Tests fuer das ``Widget``-Datenmodell."""

    def test_col_span_default_is_full_width(self) -> None:
        """Ohne col_span belegt ein Widget alle 12 Spalten."""
        assert Widget(content=p("x")).col_span == 12

    def test_accepts_component_content(self) -> None:
        """content darf auch eine Component sein, nicht nur ein Element."""
        widget = Widget(content=Badge(text="New"))
        assert isinstance(widget.content, Badge)


class TestDashboardLayout:
    """Tests fuer die ``DashboardLayout``-Komponente."""

    def test_renders_one_widget_per_entry(self) -> None:
        """Jedes Widget wird als eigene Kachel gerendert."""
        html = DashboardLayout(
            widgets=[
                Widget(title="Sales", content=p("$12,400"), col_span=4),
                Widget(title="Chart", content=p("..."), col_span=8),
            ]
        ).to_html()
        assert html.count("dashboard-widget-body") == 2
        assert "Sales" in html
        assert "Chart" in html

    def test_col_span_rendered_as_grid_column_style(self) -> None:
        """col_span wird als grid-column: span N inline-style gerendert."""
        html = DashboardLayout(widgets=[Widget(content=p("x"), col_span=4)]).to_html()
        assert "grid-column: span 4" in html

    def test_columns_sets_grid_template_columns(self) -> None:
        """columns steuert grid-template-columns auf dem Wrapper."""
        html = DashboardLayout(widgets=[], columns=6).to_html()
        assert "grid-template-columns: repeat(6, 1fr)" in html

    def test_widget_without_title_omits_title_element(self) -> None:
        """Ohne title wird kein dashboard-widget-title gerendert."""
        html = DashboardLayout(widgets=[Widget(content=p("x"))]).to_html()
        assert "dashboard-widget-title" not in html

    def test_component_content_renders_inline(self) -> None:
        """Component-Inhalte werden korrekt in die Kachel gerendert."""
        html = DashboardLayout(
            widgets=[Widget(title="Status", content=Badge(text="OK"))]
        ).to_html()
        assert '<span class="badge badge-default">OK</span>' in html

    def test_empty_widgets_renders_empty_grid(self) -> None:
        """Ohne Widgets wird ein leeres dashboard-Grid gerendert."""
        html = DashboardLayout(widgets=[]).to_html()
        assert 'class="dashboard"' in html
        assert "dashboard-widget" not in html
