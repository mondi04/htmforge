"""Shared page shell for the admin panel demo."""

from __future__ import annotations

from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import a, div, h1, main, nav, p


class BaseAdminPage(Page):
    """Full-page shell with top navigation and shared assets."""

    brand: str = "htmforge Admin Panel"
    description: str = "FastAPI + htmforge demo admin interface"
    nav_items: list[tuple[str, str]] = [("Dashboard", "/"), ("Users", "/users"), ("Settings", "/settings")]
    active_nav: str = "Dashboard"
    css_urls: list[str] = ["/static/admin.css"]
    js_urls: list[str] = ["https://unpkg.com/htmx.org@1.9.12"]

    def _render_admin_shell(self, content: list[Element | str | None]) -> list[Element | str | None]:
        """Wrap page-specific content in the shared admin shell."""
        nav_links = []
        for label, href in self.nav_items:
            cls_name = "nav-link nav-link-active" if label == self.active_nav else "nav-link"
            nav_links.append(a(label, href=href, cls=cls_name))

        return [
            div(
                div(
                    div(
                        h1(self.brand, cls="brand-title"),
                        p(self.description, cls="brand-subtitle"),
                        cls="brand-copy",
                    ),
                    nav(*nav_links, cls="nav-links"),
                    cls="topbar",
                ),
                main(*content, cls="admin-main"),
                cls="admin-app",
            )
        ]