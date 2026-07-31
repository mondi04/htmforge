"""Tests fuer ``Component.fast_construct()`` (#1)."""

from __future__ import annotations

from htmforge.components import Alert, AlertVariant


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
