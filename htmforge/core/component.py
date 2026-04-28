"""Component-Basisklasse für htmforge.

Stellt :class:`Component` bereit — eine abstrakte Pydantic-BaseModel-Klasse,
die Props-Validierung und HTML-Rendering kombiniert.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from htmforge.core.element import Element
from htmforge.htmx import HxPushUrl, HxSwap, HxTarget, HxTrigger


class Component(BaseModel, ABC):
    """Abstrakte Basisklasse für wiederverwendbare UI-Komponenten.

    Subklassen deklarieren typisierte Props als Pydantic-Felder und
    implementieren die :meth:`render`-Methode, die ein
    :class:`~htmforge.core.element.Element` zurückgibt.

    Die Klasse aktiviert Pydantic-Features:
        - ``validate_assignment = True``: Props werden auch nach der
          Initialisierung validiert.
        - ``arbitrary_types_allowed = True``: Erlaubt Non-Pydantic-Typen
          wie DOM-Elemente als Felder.
        - ``frozen = False``: Komponenten sind per Default mutable.

    Example:
        >>> from htmforge.elements import div, p
        >>>
        >>> class Card(Component):
        ...     title: str
        ...     body: str
        ...
        ...     def render(self) -> Element:
        ...         return div(p(self.title), p(self.body), cls="card")
        ...
        >>> Card(title="Hallo", body="Welt").to_html()
        '<div class="card"><p>Hallo</p><p>Welt</p></div>'
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )
    __htmforge_missing_render__: ClassVar[bool] = False

    # Typisierte HTMX-Props, die komponentenweit wiederverwendbar sind.
    hx_get: str | None = None
    hx_post: str | None = None
    hx_put: str | None = None
    hx_patch: str | None = None
    hx_delete: str | None = None
    hx_trigger: HxTrigger | str | None = None
    hx_target: HxTarget | str | None = None
    hx_swap: HxSwap | None = None
    hx_push_url: HxPushUrl | str | None = None
    hx_confirm: str | None = None
    hx_indicator: str | None = None
    hx_include: str | None = None
    hx_vals: str | dict[str, Any] | None = None
    hx_headers: str | dict[str, Any] | None = None
    hx_request: str | dict[str, Any] | None = None
    hx_select: str | None = None
    hx_select_oob: str | None = None
    hx_params: str | None = None
    hx_encoding: str | None = None

    def __init_subclass__(cls, **kwargs: Any) -> None:  # noqa: ANN401
        """Validiert, dass Unterklassen eine konkrete ``render``-Methode haben."""
        super().__init_subclass__(**kwargs)
        if cls is Component:
            return
        if cls.render is Component.render:
            cls.__htmforge_missing_render__ = True
        else:
            cls.__htmforge_missing_render__ = False

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialisiert die Komponente und blockiert Klassen ohne ``render``."""
        if getattr(type(self), "__htmforge_missing_render__", False):
            raise TypeError(
                f"Can't instantiate abstract class {type(self).__name__} "
                "without a concrete render() implementation"
            )
        super().__init__(**data)

    def __repr__(self) -> str:
        """Gibt eine lesbare Debug-Darstellung der Komponente zurueck.

        Example:
            >>> Card(title="Hi", body="World")
            Card(title='Hi', body='World')
        """
        fields = type(self).model_fields
        props = ", ".join(
            f"{k}={getattr(self, k)!r}"
            for k in fields
            if getattr(self, k) != fields[k].default
        )
        return f"{type(self).__name__}({props})"

    @abstractmethod
    def render(self) -> Element:
        """Rendert die Komponente zu einem :class:`~htmforge.core.element.Element`.

        Subklassen müssen diese Methode implementieren und das Root-Element
        der Komponente zurückgeben.

        Returns:
            Das Root-:class:`~htmforge.core.element.Element` der Komponente.
        """
        ...

    def to_html(self) -> str:
        """Delegiert das HTML-Rendering an :meth:`render`.

        Returns:
            Den vollständigen HTML-String der Komponente.
        """
        return self.render().to_html()

    def htmx_attrs(self) -> dict[str, object]:
        """Gibt alle gesetzten HTMX-Props als Attribut-Dict zurueck.

        Returns:
            Ein Dict mit nur den HTMX-Attributen, die nicht ``None`` sind.

        Example:
            ``button("Save", **self.htmx_attrs())``
        """
        attrs: dict[str, object] = {}
        for key in (
            "hx_get",
            "hx_post",
            "hx_put",
            "hx_patch",
            "hx_delete",
            "hx_trigger",
            "hx_target",
            "hx_swap",
            "hx_push_url",
            "hx_confirm",
            "hx_indicator",
            "hx_include",
            "hx_vals",
            "hx_headers",
            "hx_request",
            "hx_select",
            "hx_select_oob",
            "hx_params",
            "hx_encoding",
        ):
            value = getattr(self, key)
            if value is not None:
                attrs[key] = _normalize_htmx_value(value)
        return attrs

    # ------------------------------------------------------------------
    # Framework-Adapter (Stubs — werden in Phase 1 ausgebaut)
    # ------------------------------------------------------------------

    def to_fastapi(self) -> Any:  # noqa: ANN401
        """Gibt eine FastAPI-kompatible ``HTMLResponse`` zurück.

        Note:
            Erfordert ``fastapi`` als optionale Dependency.

        Returns:
            Eine ``fastapi.responses.HTMLResponse`` mit dem gerenderten HTML.

        Raises:
            ImportError: Wenn ``fastapi`` nicht installiert ist.
        """
        try:
            from fastapi.responses import HTMLResponse
        except ImportError as exc:
            raise ImportError(
                "fastapi ist nicht installiert. Installiere es mit: pip install fastapi"
            ) from exc
        return HTMLResponse(content=self.to_html())

    def to_flask(self) -> Any:  # noqa: ANN401
        """Gibt eine Flask-kompatible Response zurück.

        Note:
            Erfordert ``flask`` als optionale Dependency.

        Returns:
            Eine ``flask.Response`` mit dem gerenderten HTML.

        Raises:
            ImportError: Wenn ``flask`` nicht installiert ist.
        """
        try:
            from flask import Response
        except ImportError as exc:
            raise ImportError(
                "flask ist nicht installiert. Installiere es mit: pip install flask"
            ) from exc
        return Response(response=self.to_html(), mimetype="text/html")

    def to_django(self) -> Any:  # noqa: ANN401
        """Gibt eine Django-kompatible ``HttpResponse`` zurück.

        Note:
            Erfordert ``django`` als optionale Dependency.

        Returns:
            Eine ``django.http.HttpResponse`` mit dem gerenderten HTML.

        Raises:
            ImportError: Wenn ``django`` nicht installiert ist.
        """
        try:
            from django.http import HttpResponse
        except ImportError as exc:
            raise ImportError(
                "django ist nicht installiert. Installiere es mit: pip install django"
            ) from exc
        return HttpResponse(content=self.to_html())


def _normalize_htmx_value(value: object) -> object:
    """Normalisiert HTMX-Prop-Werte in HTML-kompatible Attributwerte.

    Dict-Werte werden als kompakter JSON-String serialisiert, damit
    HTMX-Attribute wie ``hx-headers``, ``hx-request`` und ``hx-vals``
    korrekt gerendert werden.

    Args:
        value: Der rohe Prop-Wert.

    Returns:
        Ein HTML-Attribut-kompatibler Wert.
    """
    if isinstance(value, dict):
        return json.dumps(value, separators=(",", ":"), sort_keys=True)
    return value
