"""Tailwind-CSS-Starter-Kit fuer htmforge (#6, bewusst reduzierter Scope).

Ein vollstaendiges Ecosystem-Package (eigenes PyPI-Paket ``htmforge-ui``,
Theming-System, 15+ Komponenten, siehe Issue) ist ein eigenstaendiges
Projekt und sprengt den Rahmen eines einzelnen Fixes in diesem Repository.
Dieses Modul liefert stattdessen einen kleinen, **optionalen** Startpunkt
mit denselben vier Bausteinen aus dem Issue-Beispiel — ``Button``, ``Card``,
``Alert``, ``Badge`` — gestylt mit Tailwind-Utility-Klassen statt der
generischen BEM-artigen Klassen aus ``htmforge.components``.

Bewusst NICHT von ``htmforge.components`` re-exportiert: wer kein Tailwind
einsetzt, soll keine Tailwind-spezifischen Klassennamen im HTML sehen. Wer
diese Variante will, importiert explizit aus ``htmforge.contrib.tailwind``.

Caveat — Tailwind JIT/Safelist:
    Die Farbklassen werden zur Laufzeit aus ``Color`` zusammengesetzt
    (``f"bg-{color}-600"``). Tailwinds JIT-Compiler erkennt Klassennamen
    nur, wenn sie als vollstaendiger String irgendwo im Quellcode
    auftauchen — rein dynamisch gebaute Strings wie hier werden vom Scanner
    **nicht** gefunden und muessen daher explizit in ``tailwind.config.js``
    als ``safelist`` eingetragen werden, sonst fehlt das CSS im Build.

Example:
    >>> from htmforge.contrib.tailwind import Button, Color
    >>> "bg-blue-600" in Button(label="Save", color=Color.BLUE).to_html()
    True
"""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import button as _button
from htmforge.elements import div, p, span


class Color(StrEnum):
    """Tailwind-Farbpalette, wie in der Issue-Vorlage skizziert."""

    SLATE = "slate"
    RED = "red"
    ORANGE = "orange"
    AMBER = "amber"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    INDIGO = "indigo"
    PURPLE = "purple"
    PINK = "pink"


class ButtonVariant(StrEnum):
    """Visuelle Button-Varianten."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    OUTLINE = "outline"


class ButtonSize(StrEnum):
    """Button-Groessen."""

    SM = "sm"
    MD = "md"
    LG = "lg"


_BUTTON_SIZE_CLASSES: dict[ButtonSize, str] = {
    ButtonSize.SM: "px-2.5 py-1.5 text-sm",
    ButtonSize.MD: "px-4 py-2 text-sm",
    ButtonSize.LG: "px-5 py-3 text-base",
}

_BUTTON_BASE_CLASSES = (
    "inline-flex items-center justify-center rounded-md font-medium "
    "transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
)


class Button(Component):
    """Tailwind-gestylter Button mit Variant/Size/Color-Props.

    Fields:
        label: str — Button-Text
        variant: ButtonVariant — primary/secondary/outline, default PRIMARY
        size: ButtonSize — sm/md/lg, default MD
        color: Color — Tailwind-Farbfamilie, default BLUE
        type: str — HTML button type, default "button"
    """

    label: str
    variant: ButtonVariant = ButtonVariant.PRIMARY
    size: ButtonSize = ButtonSize.MD
    color: Color = Color.BLUE
    type: str = "button"

    def render(self) -> Element:
        """Erstellt einen ``<button>`` mit zusammengesetzten Tailwind-Klassen."""
        size_cls = _BUTTON_SIZE_CLASSES[self.size]
        color = self.color.value

        if self.variant is ButtonVariant.PRIMARY:
            variant_cls = (
                f"bg-{color}-600 text-white hover:bg-{color}-700 focus:ring-{color}-500"
            )
        elif self.variant is ButtonVariant.SECONDARY:
            variant_cls = (
                f"bg-{color}-100 text-{color}-700 hover:bg-{color}-200 "
                f"focus:ring-{color}-500"
            )
        else:
            variant_cls = (
                f"border border-{color}-600 text-{color}-600 "
                f"hover:bg-{color}-50 focus:ring-{color}-500"
            )

        return _button(
            self.label,
            type=self.type,
            cls=merge_cls(_BUTTON_BASE_CLASSES, size_cls, variant_cls, self.extra_cls),
            **self.htmx_attrs(),
        )


class Card(Component):
    """Tailwind-gestylter Card-Container mit optionalem Titel.

    Fields:
        title: str — optionaler Card-Titel, leer = kein Titel gerendert
        children: list[Element | Component | str] — Card-Inhalt
    """

    title: str = ""
    children: list[Element | Component | str] = []

    def render(self) -> Element:
        """Erstellt eine Card mit Border, Radius und Schatten."""
        body: list[Element | Component] = []
        if self.title:
            body.append(p(self.title, cls="text-lg font-semibold text-slate-900 mb-2"))
        body.extend(
            child if isinstance(child, (Element, Component)) else span(child)
            for child in self.children
        )
        return div(
            *body,
            cls=merge_cls(
                "rounded-lg border border-slate-200 bg-white p-4 shadow-sm",
                self.extra_cls,
            ),
        )


class Alert(Component):
    """Tailwind-gestylte Alert-Box.

    Fields:
        message: str — Alert-Text
        color: Color — Tailwind-Farbfamilie, default RED (Fehler-Default)
    """

    message: str
    color: Color = Color.RED

    def render(self) -> Element:
        """Erstellt eine Alert-Box mit farbabhaengigem Hintergrund/Text."""
        color = self.color.value
        return div(
            self.message,
            cls=merge_cls(
                f"rounded-md border border-{color}-200 bg-{color}-50 "
                f"px-4 py-3 text-sm text-{color}-800",
                self.extra_cls,
            ),
            role="alert",
        )


class Badge(Component):
    """Tailwind-gestyltes Badge/Tag.

    Fields:
        text: str — Badge-Inhalt
        color: Color — Tailwind-Farbfamilie, default SLATE
    """

    text: str
    color: Color = Color.SLATE

    def render(self) -> Element:
        """Erstellt ein kleines, abgerundetes Badge-Element."""
        color = self.color.value
        return span(
            self.text,
            cls=merge_cls(
                f"inline-flex items-center rounded-full bg-{color}-100 "
                f"px-2.5 py-0.5 text-xs font-medium text-{color}-800",
                self.extra_cls,
            ),
        )


__all__ = [
    "Alert",
    "Badge",
    "Button",
    "ButtonSize",
    "ButtonVariant",
    "Card",
    "Color",
]
