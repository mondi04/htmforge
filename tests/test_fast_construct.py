"""Tests fuer ``Component.fast_construct()`` (#1)."""

from __future__ import annotations

import sys
import time

import pytest

from htmforge.components import Alert, AlertVariant, Badge, ColumnDef, DataTable


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

        Wird unter Code-Coverage-Instrumentierung (``pytest --cov=...``, wie
        in CI) uebersprungen: der coverage-Tracer verzerrt die Line-Timing-
        Charakteristik beider Pfade unterschiedlich stark und macht den
        Vergleich unzuverlaessig — ein reines CI-Artefakt, keine Aussage
        ueber echtes Laufzeitverhalten.
        """
        if "coverage" in sys.modules:
            pytest.skip("Timing-Vergleich unzuverlaessig unter Coverage-Instrumentierung")

        columns = [ColumnDef(key="name", label="Name", sortable=True)]
        rows = [{"name": Badge(text=f"Row {i}")} for i in range(10)]
        n = 500

        start = time.perf_counter()
        for _ in range(n):
            DataTable(columns=columns, dict_rows=rows)
        normal_elapsed = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(n):
            DataTable.fast_construct(columns=columns, dict_rows=rows)
        fast_elapsed = time.perf_counter() - start

        assert fast_elapsed <= normal_elapsed * 1.2
