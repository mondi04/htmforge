"""Tests fuer ``htmforge.devtools`` (#5, scoped auto-reload)."""

from __future__ import annotations

import time
from pathlib import Path

from htmforge.devtools import DevReloadWatcher, dev_reload_script


class TestDevReloadWatcher:
    """Tests fuer den mtime/Groesse-basierten Versions-Hash."""

    def test_version_is_stable_without_changes(self) -> None:
        """Ohne Aenderung an den beobachteten Dateien bleibt die Version gleich."""
        watcher = DevReloadWatcher(["htmforge/core"])
        assert watcher.current_version == watcher.current_version

    def test_version_changes_when_watched_file_is_modified(
        self, tmp_path: Path
    ) -> None:
        """Eine Aenderung an einer beobachteten Datei aendert die Version."""
        target = tmp_path / "module.py"
        target.write_text("x = 1\n", encoding="utf-8")
        watcher = DevReloadWatcher([tmp_path])
        before = watcher.current_version

        time.sleep(0.05)  # Windows/NTFS mtime resolution kann grob sein
        target.write_text("x = 2\n", encoding="utf-8")
        after = watcher.current_version

        assert before != after

    def test_version_unaffected_by_unwatched_extension(self, tmp_path: Path) -> None:
        """Dateien, die nicht auf das Muster passen, werden ignoriert."""
        watcher = DevReloadWatcher([tmp_path], patterns=("*.py",))
        before = watcher.current_version

        (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")
        after = watcher.current_version

        assert before == after

    def test_accepts_single_file_path(self, tmp_path: Path) -> None:
        """Ein einzelner Datei-Pfad (kein Verzeichnis) wird ebenfalls beobachtet."""
        target = tmp_path / "single.py"
        target.write_text("x = 1\n", encoding="utf-8")
        watcher = DevReloadWatcher([target])
        before = watcher.current_version

        time.sleep(0.05)  # Windows/NTFS mtime resolution kann grob sein
        target.write_text("x = 2\n", encoding="utf-8")
        after = watcher.current_version

        assert before != after


class TestDevReloadScript:
    """Tests fuer das gerenderte Polling-Skript."""

    def test_includes_poll_url(self) -> None:
        """Die konfigurierte poll_url erscheint im Skript."""
        assert "/__htmforge_dev__/version" in dev_reload_script()

    def test_custom_poll_url_used(self) -> None:
        """Eine benutzerdefinierte poll_url wird uebernommen."""
        assert "/custom/version" in dev_reload_script(poll_url="/custom/version")

    def test_custom_interval_used(self) -> None:
        """Ein benutzerdefiniertes Intervall wird uebernommen."""
        assert "var interval=2500" in dev_reload_script(interval_ms=2500)

    def test_guarded_by_idempotency_flag(self) -> None:
        """Das Skript ist per Flag gegen doppelte Registrierung geschuetzt."""
        assert "window.__htmforgeDevReloadStarted" in dev_reload_script()

    def test_returns_script_tag(self) -> None:
        """Das Ergebnis ist ein eingebettetes <script>-Tag."""
        script = dev_reload_script()
        assert script.startswith("<script>")
        assert script.endswith("</script>")
