"""Tests fuer Component-Level Asset-Injection (#3)."""

from __future__ import annotations

from htmforge import Component
from htmforge.components.page import Page
from htmforge.core.assets import collect_assets
from htmforge.core.element import Element
from htmforge.elements import div


class ChartWidget(Component):
    """Test-Component mit deklarierten Asset-Abhaengigkeiten."""

    css_files = ["chart.css"]
    js_files = ["chart.js"]
    label: str = "chart"

    def render(self) -> Element:
        return div(self.label, cls="chart")


class MapWidget(Component):
    """Zweite Test-Component mit eigenen Assets, nested innerhalb eines Elements."""

    css_files = ["map.css", "shared.css"]
    js_files = ["map.js"]

    def render(self) -> Element:
        return div(cls="map")


class PlainWidget(Component):
    """Component ohne eigene Assets (default leere Listen)."""

    def render(self) -> Element:
        return div("plain")


class TestCollectAssets:
    """Tests fuer ``collect_assets``."""

    def test_collects_top_level_component_assets(self) -> None:
        """Assets einer direkt uebergebenen Component werden gesammelt."""
        css, js = collect_assets(ChartWidget())
        assert css == ["chart.css"]
        assert js == ["chart.js"]

    def test_collects_nested_component_assets(self) -> None:
        """Assets einer tief verschachtelten Component werden gefunden."""
        tree = div(div(div(ChartWidget())))
        css, js = collect_assets(tree)
        assert css == ["chart.css"]
        assert js == ["chart.js"]

    def test_deduplicates_across_multiple_instances(self) -> None:
        """Mehrere Instanzen derselben Component erzeugen keine Duplikate."""
        css, js = collect_assets(div(ChartWidget(), ChartWidget(label="other")))
        assert css == ["chart.css"]
        assert js == ["chart.js"]

    def test_preserves_first_occurrence_order_across_components(self) -> None:
        """Reihenfolge folgt dem ersten Auftreten, Duplikate werden entfernt."""
        css, _js = collect_assets(div(ChartWidget(), MapWidget()))
        assert css == ["chart.css", "map.css", "shared.css"]

    def test_component_without_assets_contributes_nothing(self) -> None:
        """Components ohne css_files/js_files tragen nichts bei."""
        css, js = collect_assets(PlainWidget())
        assert css == []
        assert js == []

    def test_multiple_root_nodes(self) -> None:
        """Mehrere Wurzelknoten werden alle durchlaufen."""
        css, js = collect_assets(ChartWidget(), MapWidget())
        assert css == ["chart.css", "map.css", "shared.css"]
        assert js == ["chart.js", "map.js"]

    def test_none_and_str_nodes_are_ignored(self) -> None:
        """None und reine Strings werden ohne Fehler uebersprungen."""
        css, js = collect_assets(None, "plain text", ChartWidget())
        assert css == ["chart.css"]
        assert js == ["chart.js"]


class ChartPage(Page):
    """Test-Page die eine Component mit Assets einbindet."""

    def _body_content(self) -> list[Element | str | None]:
        return [ChartWidget()]


class TestPageAssetInjection:
    """Tests fuer die automatische Asset-Injection in ``Page``."""

    def test_auto_injects_component_css_as_link_tag(self) -> None:
        """css_files der Body-Components werden als <link> injiziert."""
        html_out = ChartPage(title="Dashboard").to_html()
        assert '<link rel="stylesheet" href="chart.css">' in html_out

    def test_auto_injects_component_js_as_script_tag(self) -> None:
        """js_files der Body-Components werden als <script> injiziert."""
        html_out = ChartPage(title="Dashboard").to_html()
        assert '<script src="chart.js">' in html_out

    def test_explicit_css_urls_not_duplicated(self) -> None:
        """Explizit gesetzte css_urls werden nicht doppelt injiziert."""
        html_out = ChartPage(title="Dashboard", css_urls=["chart.css"]).to_html()
        assert html_out.count('href="chart.css"') == 1

    def test_explicit_urls_rendered_before_auto_discovered(self) -> None:
        """Explizite css_urls erscheinen vor automatisch gefundenen."""
        html_out = ChartPage(title="Dashboard", css_urls=["base.css"]).to_html()
        base_pos = html_out.index('href="base.css"')
        chart_pos = html_out.index('href="chart.css"')
        assert base_pos < chart_pos
