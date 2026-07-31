"""Dev-Mode Auto-Reload fuer htmforge (#5, bewusst reduzierter Scope).

Volles WebSocket-basiertes Component-Hot-Swapping mit State-Erhalt (wie im
Issue vorgeschlagen) braucht clientseitiges DOM-Patching (z.B. Morphdom) und
wuerde eine harte neue Abhaengigkeit einfuehren — das widerspricht
htmforges eigener "keine JS-Abhaengigkeiten"-Praemisse (siehe #6) und ist
fuer einen einzelnen Umsetzungsschritt zu groß. Dieses Modul liefert
stattdessen eine bewusst simple, abhaengigkeitsfreie Variante:

- :class:`DevReloadWatcher` berechnet einen billigen Versions-Hash ueber
  beobachtete Quelldateien (mtime + Groesse, kein Datei-Read).
- :func:`dev_reload_script` rendert ein kleines Skript, das diesen Hash
  periodisch von einem selbst gehosteten Endpunkt pollt und bei Aenderung
  ``location.reload()`` ausloest.

Nur in ``DEBUG``/Dev-Betrieb einbinden — kein State-Erhalt, volle
Seiten-Reloads statt gezieltem DOM-Patching. Ein spaeterer Ausbau zu
WebSocket-Push + partiellem Swap ist damit nicht ausgeschlossen, sondern
bewusst als naechster Schritt offen gelassen.

Example:
    >>> from htmforge.devtools import DevReloadWatcher, dev_reload_script
    >>> watcher = DevReloadWatcher(["htmforge"])
    >>> isinstance(watcher.current_version, str)
    True
    >>> "__htmforgeDevReloadStarted" in dev_reload_script()
    True
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Iterator
from pathlib import Path

from markupsafe import Markup

from htmforge.elements import raw


class DevReloadWatcher:
    """Berechnet einen Versions-Hash ueber beobachtete Quelldateien.

    Hasht Dateipfad + mtime + Groesse statt des Dateiinhalts — deutlich
    billiger bei haeufigem Polling und ausreichend genau, um Aenderungen
    waehrend der Entwicklung zuverlaessig zu erkennen.

    Args:
        paths: Verzeichnisse oder einzelne Dateien, die beobachtet werden.
        patterns: Glob-Muster fuer die Dateisuche in Verzeichnissen,
            default ``("*.py",)``.

    Example:
        >>> watcher = DevReloadWatcher(["htmforge"], patterns=("*.py",))
        >>> v1 = watcher.current_version
        >>> v1 == watcher.current_version
        True
    """

    def __init__(
        self,
        paths: Iterable[str | Path],
        patterns: tuple[str, ...] = ("*.py",),
    ) -> None:
        """Initialisiert den Watcher mit den zu beobachtenden Pfaden."""
        self.paths = [Path(p) for p in paths]
        self.patterns = patterns

    def _iter_files(self) -> Iterator[Path]:
        """Liefert alle beobachteten Dateien (Verzeichnisse rekursiv)."""
        for base in self.paths:
            if base.is_file():
                yield base
                continue
            for pattern in self.patterns:
                yield from base.rglob(pattern)

    @property
    def current_version(self) -> str:
        """Aktueller Versions-Hash ueber alle beobachteten Dateien.

        Returns:
            Ein 16-stelliger Hex-String, der sich aendert sobald sich
            mtime oder Groesse einer beobachteten Datei aendert (oder eine
            Datei hinzukommt/verschwindet).
        """
        digest = hashlib.sha256()
        for file in sorted(self._iter_files()):
            try:
                stat = file.stat()
            except OSError:
                continue
            digest.update(f"{file}:{stat.st_mtime_ns}:{stat.st_size}".encode())
        return digest.hexdigest()[:16]


def dev_reload_script(
    poll_url: str = "/__htmforge_dev__/version",
    interval_ms: int = 1000,
) -> Markup:
    """Rendert ein Skript, das per Polling einen Full-Page-Reload ausloest.

    Ruft ``poll_url`` periodisch per ``fetch`` ab (erwartet die
    :attr:`DevReloadWatcher.current_version` als Plaintext-Response) und
    reloadet die Seite, sobald sich der Wert gegenueber dem letzten Poll
    aendert. Netzwerkfehler werden stillschweigend ignoriert (z.B. Server
    startet gerade neu), damit kurze Downtime waehrend Reloads kein Rauschen
    in der Konsole erzeugt.

    Args:
        poll_url: Endpunkt, der den aktuellen
            :attr:`DevReloadWatcher.current_version`-Wert als Plaintext
            liefert.
        interval_ms: Polling-Intervall in Millisekunden, default 1000.

    Returns:
        Ein :class:`markupsafe.Markup`-Objekt mit dem ``<script>``-Tag,
        einbettbar wie jedes andere ``raw()``-Fragment.

    Example:
        In der eigenen ``Page``-Subklasse, nur wenn ``settings.DEBUG``::

            def _body_content(self):
                content = [...]
                if settings.DEBUG:
                    content.append(dev_reload_script())
                return content
    """
    return raw(
        "<script>"
        "if(!window.__htmforgeDevReloadStarted){"
        "window.__htmforgeDevReloadStarted=true;"
        "(function(){"
        f"var url={poll_url!r};"
        f"var interval={int(interval_ms)};"
        "var current=null;"
        "function poll(){"
        "fetch(url).then(function(r){return r.text();}).then(function(v){"
        "if(current===null){current=v;}"
        "else if(v!==current){location.reload();}"
        "}).catch(function(){});"
        "}"
        "setInterval(poll,interval);"
        "poll();"
        "})();"
        "}"
        "</script>"
    )


__all__ = ["DevReloadWatcher", "dev_reload_script"]
