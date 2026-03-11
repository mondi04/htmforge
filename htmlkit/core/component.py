"""Component-Basisklasse für htmlkit.

Stellt :class:`Component` bereit — eine abstrakte Pydantic-BaseModel-Klasse,
die Props-Validierung und HTML-Rendering kombiniert.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict

from htmlkit.core.element import Element


class Component(BaseModel):
    """Abstrakte Basisklasse für wiederverwendbare UI-Komponenten.

    Subklassen deklarieren typisierte Props als Pydantic-Felder und
    implementieren die :meth:`render`-Methode, die ein :class:`~htmlkit.core.element.Element`
    zurückgibt.

    Die Klasse aktiviert Pydantic-Features:
        - ``validate_assignment = True``: Props werden auch nach der
          Initialisierung validiert.
        - ``arbitrary_types_allowed = True``: Erlaubt Non-Pydantic-Typen
          wie DOM-Elemente als Felder.
        - ``frozen = False``: Komponenten sind per Default mutable.

    Example:
        >>> from htmlkit.elements import div, p
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

    @abstractmethod
    def render(self) -> Element:
        """Rendert die Komponente zu einem :class:`~htmlkit.core.element.Element`.

        Subklassen müssen diese Methode implementieren und das Root-Element
        der Komponente zurückgeben.

        Returns:
            Das Root-:class:`~htmlkit.core.element.Element` der Komponente.
        """
        ...

    def to_html(self) -> str:
        """Delegiert das HTML-Rendering an :meth:`render`.

        Returns:
            Den vollständigen HTML-String der Komponente.
        """
        return self.render().to_html()

    # ------------------------------------------------------------------
    # Framework-Adapter (Stubs — werden in Phase 1 ausgebaut)
    # ------------------------------------------------------------------

    def to_fastapi(self) -> Any:
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
                "fastapi ist nicht installiert. "
                "Installiere es mit: pip install fastapi"
            ) from exc
        return HTMLResponse(content=self.to_html())

    def to_flask(self) -> Any:
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
                "flask ist nicht installiert. "
                "Installiere es mit: pip install flask"
            ) from exc
        return Response(response=self.to_html(), mimetype="text/html")

    def to_django(self) -> Any:
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
                "django ist nicht installiert. "
                "Installiere es mit: pip install django"
            ) from exc
        return HttpResponse(content=self.to_html())
