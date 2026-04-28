from htmforge.htmx import hx_keyup_delay


def test_hx_keyup_delay_default() -> None:
    assert hx_keyup_delay() == "keyup delay:300ms"


def test_hx_keyup_delay_custom() -> None:
    assert hx_keyup_delay(500) == "keyup delay:500ms"
