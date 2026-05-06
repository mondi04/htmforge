"""Performance-Benchmark: render-Zeit fuer 1000 Elemente.

Kein externes Tool noetig - misst mit time.perf_counter.
Schlaegt fehl wenn render Zeit > 1 Sekunde fuer 1000 Durchlaeufe.
"""

from __future__ import annotations

import time

from htmforge import render
from htmforge.components import Alert, DataTable
from htmforge.elements import div, li, p, ul


def test_element_render_1000_times_under_1s() -> None:
    """1000 div-Renders muessen unter 1 Sekunde dauern."""
    start = time.perf_counter()
    for _ in range(1000):
        div(p("Hello"), p("World"), cls="container").to_html()
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s for 1000 renders"


def test_nested_element_render_1000_times_under_1s() -> None:
    """1000 verschachtelte ul/li Renders unter 1 Sekunde."""
    start = time.perf_counter()
    for _ in range(1000):
        ul(*[li(f"Item {i}") for i in range(20)]).to_html()
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s"


def test_datatable_render_1000_times_under_2s() -> None:
    """1000 DataTable-Renders (10 Zeilen) unter 2 Sekunden."""
    rows = [[f"Name {i}", f"email{i}@example.com"] for i in range(10)]
    start = time.perf_counter()
    for _ in range(1000):
        DataTable(headers=["Name", "Email"], rows=rows).to_html()
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0, f"Too slow: {elapsed:.3f}s"


def test_alert_render_1000_times_under_1s() -> None:
    """1000 Alert-Renders unter 1 Sekunde."""
    start = time.perf_counter()
    for _ in range(1000):
        Alert(message="Gespeichert", dismissible=True).to_html()
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s"


def test_render_function_1000_components_under_1s() -> None:
    """render() top-level: 1000 Aufrufe unter 1 Sekunde."""
    start = time.perf_counter()
    for _ in range(1000):
        render(div("x"))
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s"
