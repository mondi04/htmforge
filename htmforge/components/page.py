"""Vollstaendige HTML-Seiten-Komponente fuer htmforge.

Example:
    >>> from htmforge.components.page import Page
    >>> from htmforge.core.element import Element
    >>>
    >>> class IndexPage(Page):
    ...     def _body_content(self) -> list[Element | str | None]:
    ...         return []
    ...
    >>> html = IndexPage(title="Start").to_html()
    >>> html.startswith("<!DOCTYPE html>")
    True
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from htmforge import Component
from htmforge.core.assets import collect_assets
from htmforge.core.element import Element
from htmforge.elements import (
    body,
    head,
    html,
    link,
    meta,
    raw,
    script,
    style,
    title,
)


class Page(Component):
    """Abstrakte Basisklasse fuer vollstaendige HTML-Dokumente mit DOCTYPE.

    Subklassen implementieren :meth:`_body_content` um den Seiteninhalt
    bereitzustellen. :meth:`to_html` haengt automatisch ``<!DOCTYPE html>``
    voran.

    Example:
        >>> from htmforge.components.page import Page
        >>> from htmforge.core.element import Element
        >>>
        >>> class MyPage(Page):
        ...     users: list[str] = []
        ...
        ...     def _body_content(self) -> list[Element | str | None]:
        ...         from htmforge.elements import li, ul
        ...         return [ul(*[li(u) for u in self.users])]
        ...
        >>> page = MyPage(title="Users", users=["Ada", "Grace"])
        >>> page.to_html().startswith("<!DOCTYPE html>")
        True
    """

    title: str
    description: str = ""
    css_urls: list[str] = []
    js_urls: list[str] = []
    inline_css: str = ""
    charset: str = "utf-8"
    lang: str = "en"

    @abstractmethod
    def _body_content(self) -> list[Element | str | None]:
        """Liefert die Kinder des ``<body>``-Elements.

        Returns:
            Eine Liste von Elementen, Strings oder None-Werten.
        """
        ...

    def render(self) -> Element:
        """Rendert das vollstaendige ``<html>``-Dokument ohne DOCTYPE.

        Sammelt zusaetzlich zu den explizit gesetzten ``css_urls``/``js_urls``
        automatisch die ``css_files``/``js_files`` aller Components im
        Seiteninhalt (#3, siehe :func:`~htmforge.core.assets.collect_assets`)
        und injiziert sie dedupliziert — Components bleiben so unabhaengig
        von der Seite, die sie einbindet, selbst-beschreibend.
        """
        head_children: list[Any] = [meta(charset=self.charset)]

        if self.description:
            head_children.append(meta(name="description", content=self.description))

        head_children.append(title(self.title))

        body_children: list[Any] = [c for c in self._body_content() if c is not None]
        auto_css, auto_js = collect_assets(*body_children)

        seen_css = set(self.css_urls)
        for css_url in self.css_urls:
            head_children.append(link(rel="stylesheet", href=css_url))
        for css_url in auto_css:
            if css_url not in seen_css:
                seen_css.add(css_url)
                head_children.append(link(rel="stylesheet", href=css_url))

        if self.inline_css:
            head_children.append(style(raw(self.inline_css)))

        seen_js = set(self.js_urls)
        for js_url in self.js_urls:
            body_children.append(script(src=js_url))
        for js_url in auto_js:
            if js_url not in seen_js:
                seen_js.add(js_url)
                body_children.append(script(src=js_url))

        return html(
            head(*head_children),
            body(*body_children),
            lang=self.lang,
        )

    def to_html(self) -> str:
        """Rendert das vollstaendige Dokument inklusive ``<!DOCTYPE html>``."""
        return "<!DOCTYPE html>" + self.render().to_html()
