"""HTMX-Typen und Enums für htmforge.

Stellt typisierte Enumerationen für HTMX-Attribute bereit, damit
HTMX-Konfigurationen in Komponenten-Props genutzt werden können —
ohne Strings per Hand eintippen zu müssen.

Alle Werte entsprechen den offiziellen HTMX-Attribut-Werten (kebab-case
bzw. Kleinbuchstaben) wie in der HTMX-Dokumentation definiert.

Example::

    from htmforge.elements import button
    from htmforge.htmx import HxSwap

    btn = button(
        "Löschen",
        hx_delete="/users/1",
        hx_swap=HxSwap.OUTER_HTML,
        hx_confirm="Wirklich löschen?",
    )
"""

from __future__ import annotations

from enum import StrEnum


class HxSwap(StrEnum):
    """Typisierter Enum für das ``hx-swap``-Attribut.

    Bestimmt, wie HTMX den zurückgegebenen HTML-Inhalt in den DOM einfügt.

    See: https://htmx.org/attributes/hx-swap/
    """

    INNER_HTML = "innerHTML"
    """Ersetzt den inneren HTML-Inhalt des Ziel-Elements (Standard)."""

    OUTER_HTML = "outerHTML"
    """Ersetzt das Ziel-Element vollständig inkl. Tag."""

    BEFORE_BEGIN = "beforebegin"
    """Fügt den Inhalt vor dem Ziel-Element ein."""

    AFTER_BEGIN = "afterbegin"
    """Fügt den Inhalt als erstes Kind des Ziel-Elements ein."""

    BEFORE_END = "beforeend"
    """Fügt den Inhalt als letztes Kind des Ziel-Elements ein."""

    AFTER_END = "afterend"
    """Fügt den Inhalt nach dem Ziel-Element ein."""

    DELETE = "delete"
    """Löscht das Ziel-Element ohne Ersatz."""

    NONE = "none"
    """Führt keinen DOM-Swap durch (z.B. nur Out-of-Band-Swaps)."""


class HxTrigger(StrEnum):
    """Typisierter Enum für häufige ``hx-trigger``-Werte.

    Legt fest, welches Ereignis einen HTMX-Request auslöst.

    Note:
        Für komplexe Trigger-Ausdrücke (z.B. ``"click delay:500ms"``)
        muss ein roher String verwendet werden.

    See: https://htmx.org/attributes/hx-trigger/
    """

    CLICK = "click"
    """Löst beim Klick aus (Standard für Buttons/Links)."""

    CHANGE = "change"
    """Löst bei einer Wertänderung aus (Standard für Inputs)."""

    SUBMIT = "submit"
    """Löst beim Absenden eines Formulars aus."""

    KEYUP = "keyup"
    """Löst bei jedem Tastenleseereignis aus."""

    LOAD = "load"
    """Löst einmalig aus, wenn das Element geladen wird."""

    REVEALED = "revealed"
    """Löst aus, wenn das Element in den sichtbaren Bereich gescrollt wird."""

    INTERSECT = "intersect"
    """Löst aus, wenn das Element den Viewport schneidet (Intersection Observer)."""

    EVERY_1S = "every 1s"
    """Löst periodisch jede Sekunde aus."""

    EVERY_2S = "every 2s"
    """Löst periodisch alle 2 Sekunden aus."""


class HxTarget(StrEnum):
    """Typisierter Enum für häufige ``hx-target``-Werte.

    Bestimmt, welches Element als Ziel für einen HTMX-Swap verwendet wird.

    Note:
        Für CSS-Selektor-Targets (z.B. ``"#my-div"``, ``".container"``)
        muss ein roher String verwendet werden.

    See: https://htmx.org/attributes/hx-target/
    """

    THIS = "this"
    """Das Element selbst, das den Request ausgelöst hat."""

    CLOSEST_TR = "closest tr"
    """Die nächste übergeordnete Tabellenzeile."""

    CLOSEST_DIV = "closest div"
    """Das nächste übergeordnete ``<div>``-Element."""

    NEXT = "next"
    """Das unmittelbar folgende Geschwister-Element."""

    PREVIOUS = "previous"
    """Das unmittelbar vorherige Geschwister-Element."""


class HxPushUrl(StrEnum):
    """Typisierter Enum für das ``hx-push-url``-Attribut.

    Steuert, ob die URL in der Browser-History aktualisiert wird.

    See: https://htmx.org/attributes/hx-push-url/
    """

    TRUE = "true"
    """Schiebt die Request-URL in die Browser-History."""

    FALSE = "false"
    """Verhindert eine URL-Änderung."""


__all__ = [
    "HxPushUrl",
    "HxSwap",
    "HxTarget",
    "HxTrigger",
]


def hx_keyup_delay(ms: int = 300) -> str:
    """Erzeugt einen HTMX keyup-Trigger-String mit Debounce-Delay.

    Args:
        ms: Wartezeit in Millisekunden nach dem letzten Tastendruck.

    Returns:
        Einen HTMX-kompatiblen Trigger-String, z.B. "keyup delay:300ms".

    Example:
        >>> from htmforge.htmx import hx_keyup_delay
        >>> hx_keyup_delay(500)
        'keyup delay:500ms'
    """
    return f"keyup delay:{ms}ms"


# Export helper in the public API
__all__.append("hx_keyup_delay")
