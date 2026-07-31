"""Component-Basisklasse für htmforge.

Stellt :class:`Component` bereit — eine abstrakte Pydantic-BaseModel-Klasse,
die Props-Validierung und HTML-Rendering kombiniert.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from copy import deepcopy
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

    # Component-Level Asset-Injection (#3): Subklassen deklarieren ihre
    # eigenen CSS-/JS-Abhaengigkeiten hier statt sie manuell auf Seitenebene
    # zu verdrahten. ``htmforge.core.assets.collect_assets`` sammelt diese
    # rekursiv und dedupliziert ueber einen ganzen Component-Baum; ``Page``
    # injiziert sie automatisch (siehe ``Page.render``).
    css_files: ClassVar[list[str]] = []
    js_files: ClassVar[list[str]] = []

    # Optionale Zusatz-CSS-Klasse, die jede Component an ihr Root-Element
    # anhängt (additiv, ersetzt nicht die Default-Klasse). Siehe
    # ``htmforge.core.element.merge_cls``.
    extra_cls: str = ""

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
        buf: list[str] = []
        self._write(buf)
        return "".join(buf)

    def _write(self, buf: list[str]) -> None:
        """Schreibt das gerenderte HTML dieser Komponente in ``buf``.

        Teil des Writer-Patterns aus :class:`~htmforge.core.element.Element`
        (#18) — Components delegieren direkt in den geteilten Puffer, statt
        einen Zwischenstring ueber :meth:`render` ``.to_html()`` zu bauen.

        Args:
            buf: Der gemeinsame Ziel-Puffer, an den angehaengt wird.
        """
        self.render()._write(buf)  # noqa: SLF001

    def clone(self, **overrides: Any) -> Component:  # noqa: ANN401
        """Gibt eine neue Instanz mit geaenderten Props zurueck.

        Args:
            **overrides: Felder die ueberschrieben werden sollen.

        Returns:
            Eine neue Instanz desselben Typs mit den geaenderten Werten.

        Example:
            >>> card = GreetingCard(title="Hi", body="World")
            >>> card2 = card.clone(title="Hello")
            >>> card2.title
            'Hello'
            >>> card2.body
            'World'
        """
        data = {
            field_name: deepcopy(getattr(self, field_name))
            for field_name in type(self).model_fields
        }
        data.update(overrides)
        return type(self)(**data)

    @classmethod
    def fast_construct(cls, **data: Any) -> Component:  # noqa: ANN401
        """Erstellt eine Instanz ohne Pydantic-Validierung (Opt-in Fast-Path, #1).

        Nutzt intern ``BaseModel.model_construct()``, um den vollen
        Validierungszyklus zu ueberspringen — sinnvoll, wenn dieselbe
        Component-Struktur sehr oft mit bereits bekanntermassen gueltigen
        Daten instanziiert wird (z.B. in engen Rendering-Loops ueber
        Datenbank-Zeilen, die schon einmal validiert wurden).

        Warning:
            Die Daten werden NICHT validiert oder typ-konvertiert. Falsche
            Typen oder fehlende Pflichtfelder fuehren nicht hier, sondern
            erst (oder ueberhaupt nicht) beim Rendern zu einem Fehler. Nur
            verwenden, wenn die Gueltigkeit der Daten bereits anderweitig
            sichergestellt ist.

        Note:
            Benchmarks zeigen: fuer kleine, flache Components (wenige
            einfache Felder, z.B. ``Alert``) ist dieser Pfad tendenziell
            *langsamer* als die normale, validierte Konstruktion — Pydantic
            v2 validiert einfache Modelle bereits ueber den kompilierten
            Rust-Core, waehrend ``model_construct()`` reiner Python-Code
            ist. Der Vorteil zeigt sich erst bei Components mit
            aufwendigerer Struktur (verschachtelte Submodelle, laengere
            Listen — z.B. ``DataTable`` mit vielen ``dict_rows``), wo die
            Validierungskosten mit der Struktur wachsen, der
            Python-Overhead von ``model_construct()`` aber ungefaehr
            konstant bleibt. Vor dem Einsatz in einem Hot-Loop lohnt sich
            ein Benchmark der konkreten Component.

        Args:
            **data: Feldwerte, unvalidiert uebernommen. Fehlende Felder
                erhalten ihren deklarierten Default, soweit vorhanden.

        Returns:
            Eine neue Instanz, ohne dass Pydantic-Validierung durchlaufen
            wurde.

        Example:
            >>> card = GreetingCard.fast_construct(title="Hi")
            >>> card.title
            'Hi'
        """
        if getattr(cls, "__htmforge_missing_render__", False):
            raise TypeError(
                f"Can't instantiate abstract class {cls.__name__} "
                "without a concrete render() implementation"
            )
        return cls.model_construct(**data)

    def to_fragment(self) -> str:
        """Rendert die Komponente als HTMX-Fragment (identisch mit to_html()).

        Explizite Methode fuer Fragmente um die Absicht zu dokumentieren:
        dieser Endpunkt liefert kein vollstaendiges Dokument, sondern nur
        einen HTML-Ausschnitt fuer HTMX-Swaps.

        Returns:
            Den HTML-String der Komponente ohne DOCTYPE.

        Example:
            >>> Alert(message="OK").to_fragment()
            '<div class="alert alert-info">OK</div>'
        """
        return self.to_html()

    def to_json(self) -> dict[str, str]:
        """Return a JSON-serializable dict with HTML and component metadata.

        This is useful for API endpoints that need to return a rendered HTML
        fragment alongside minimal metadata about the component instance.

        Returns:
            A mapping containing the rendered HTML under ``"html"`` and the
            component class name under ``"component"``.

        Example:
            >>> card = GreetingCard(title="Hi")
            >>> card.to_json()
            {'html': '<div class="card">Hi</div>', 'component': 'GreetingCard'}
        """
        return {"html": self.to_html(), "component": type(self).__name__}

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
