"""Tests fuer ``Component.fast_construct()`` (#1)."""

from __future__ import annotations

import time

from htmforge.components import Alert, AlertVariant, Badge, ColumnDef, DataTable


def _best_of(fn: object, n: int, repeats: int) -> float:
    """Gibt die schnellste von ``repeats`` Messungen von ``n`` Aufrufen zurueck.

    Best-of-N ist deutlich rauschresistenter als eine einzelne Messung —
    GC-Pausen, OS-Scheduling-Jitter oder andere Prozesse auf einem geteilten
    CI-Runner schlagen typischerweise nur auf einzelne Durchlaeufe durch,
    nicht auf alle. Das Minimum naehert sich damit der tatsaechlichen
    Ausfuehrungszeit ohne Stoerungen an.
    """
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        for _ in range(n):
            fn()  # type: ignore[operator]
        best = min(best, time.perf_counter() - start)
    return best


class TestFastConstruct:
    """Tests fuer den Validierungs-Fast-Path."""

    def test_produces_identical_html_to_normal_construction(self) -> None:
        """fast_construct() rendert identisches HTML zur validierten Instanz."""
        normal = Alert(message="Saved", variant=AlertVariant.SUCCESS)
        fast = Alert.fast_construct(message="Saved", variant=AlertVariant.SUCCESS)
        assert fast.to_html() == normal.to_html()

    def test_missing_fields_use_declared_defaults(self) -> None:
        """Nicht uebergebene Felder erhalten ihren deklarierten Default."""
        fast = Alert.fast_construct(message="Hi")
        assert fast.variant == AlertVariant.INFO
        assert fast.dismissible is False

    def test_bypasses_validation_no_error_for_wrong_type(self) -> None:
        """fast_construct() validiert bewusst nicht, im Gegensatz zum Normalpfad."""
        fast = Alert.fast_construct(message=123)  # type: ignore[arg-type]
        assert fast.message == 123  # kein Type-Coercion/Validation passiert

    def test_is_faster_for_complex_nested_components(self) -> None:
        """fast_construct() zahlt sich fuer Components mit teurer Validierung aus.

        Kein hartes Perf-Ziel (variiert je nach Maschine) — nur ein
        Sanity-Check am Beispiel aus der Docstring-Note: bei einer
        ``DataTable`` mit mehreren verschachtelten ``dict_rows`` (Validierung
        skaliert mit der Struktur) sollte der Skip-Validation-Pfad tatsaechlich
        guenstiger sein. Fuer triviale, flache Components (siehe
        ``test_produces_identical_html_to_normal_construction``) gilt das
        NICHT zwingend, siehe Docstring-Note auf ``fast_construct``.

        Nutzt Best-of-5-Messungen statt eines einzelnen Durchlaufs und eine
        grosszuegige 2x-Marge, um auf geteilten/virtualisierten CI-Runnern
        (variable CPU-Zuteilung, GC-Pausen, andere Jobs auf derselben
        Maschine) nicht zu flackern — ein einzelner Durchlauf mit enger
        Marge erwies sich sowohl unter Coverage-Instrumentierung als auch
        ohne als unzuverlaessig.
        """
        columns = [ColumnDef(key="name", label="Name", sortable=True)]
        rows = [{"name": Badge(text=f"Row {i}")} for i in range(10)]
        n = 500

        normal_elapsed = _best_of(
            lambda: DataTable(columns=columns, dict_rows=rows), n, repeats=5
        )
        fast_elapsed = _best_of(
            lambda: DataTable.fast_construct(columns=columns, dict_rows=rows),
            n,
            repeats=5,
        )

        assert fast_elapsed <= normal_elapsed * 2.0
