"""Unit-Tests fuer Komponenten aus htmforge v0.2.0."""

from __future__ import annotations

import pytest

from htmforge.components import (
    Badge,
    BadgeVariant,
    Breadcrumb,
    BreadcrumbItem,
    Modal,
    Spinner,
    SpinnerSize,
)
from htmforge.elements import button, p


def test_badge_default_variant() -> None:
    """Badge nutzt ohne Variant-Prop die Default-Klasse."""
    html = Badge(text="Neu").to_html()
    assert html == '<span class="badge badge--default">Neu</span>'


def test_badge_success() -> None:
    """Badge rendert die SUCCESS-Variante als CSS-Klasse."""
    html = Badge(text="OK", variant=BadgeVariant.SUCCESS).to_html()
    assert html == '<span class="badge badge--success">OK</span>'


def test_badge_escapes_html() -> None:
    """Badge escaped Sonderzeichen im Text-Inhalt."""
    html = Badge(text="<b>x</b>").to_html()
    assert "&lt;b&gt;x&lt;/b&gt;" in html
    assert "<b>x</b>" not in html


def test_breadcrumb_with_links() -> None:
    """Breadcrumb rendert Links und markiert das letzte Item als active."""
    html = Breadcrumb(
        items=[
            BreadcrumbItem(label="Home", href="/home"),
            BreadcrumbItem(label="Settings", href="/settings"),
            BreadcrumbItem(label="Profil"),
        ]
    ).to_html()

    assert html.startswith('<nav class="breadcrumb" aria-label="breadcrumb">')
    assert '<a href="/home" class="breadcrumb__link">Home</a>' in html
    assert '<a href="/settings" class="breadcrumb__link">Settings</a>' in html
    assert 'class="breadcrumb__item breadcrumb__item--active"' in html
    assert 'aria-current="page"' in html
    assert "Profil" in html


def test_breadcrumb_empty() -> None:
    """Leere Items-Liste rendert ein leeres nav ohne Listenpunkte."""
    html = Breadcrumb(items=[]).to_html()
    assert html == '<nav class="breadcrumb" aria-label="breadcrumb"></nav>'
    assert "<li" not in html


def test_breadcrumb_separator() -> None:
    """Custom-Separator wird zwischen Items als Span gerendert."""
    html = Breadcrumb(
        items=[
            BreadcrumbItem(label="A", href="/a"),
            BreadcrumbItem(label="B"),
        ],
        separator=">",
    ).to_html()
    assert '<span class="breadcrumb__separator">&gt;</span>' in html


def test_spinner_default() -> None:
    """Spinner setzt Standardgroesse und Accessibility-Attribute."""
    html = Spinner().to_html()
    assert 'class="spinner spinner--md"' in html
    assert 'role="status"' in html
    assert 'aria-label="Laden..."' in html
    assert '<span class="spinner__sr-only">Laden...</span>' in html


def test_spinner_large() -> None:
    """Spinner rendert die LG-Variante korrekt."""
    html = Spinner(size=SpinnerSize.LARGE).to_html()
    assert 'class="spinner spinner--lg"' in html


def test_modal_basic() -> None:
    """Modal rendert Header/Body und korrekte aria-Referenzen."""
    html = Modal(modal_id="my-modal", title="Titel", body=p("Body")).to_html()
    assert 'id="my-modal"' in html
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html
    assert 'aria-labelledby="my-modal__title"' in html
    assert '<h2 id="my-modal__title" class="modal__title">Titel</h2>' in html
    assert '<div class="modal__body"><p>Body</p></div>' in html


def test_modal_no_footer() -> None:
    """Ohne Footer wird kein modal__footer-Container gerendert."""
    html = Modal(modal_id="plain-modal", title="X", body="Inhalt").to_html()
    assert 'class="modal__footer"' not in html


def test_modal_with_footer() -> None:
    """Mit Footer wird ein modal__footer-Container gerendert."""
    html = Modal(
        modal_id="footer-modal",
        title="X",
        body="Inhalt",
        footer=button("OK"),
    ).to_html()
    assert '<div class="modal__footer"><button>OK</button></div>' in html


def test_modal_invalid_id() -> None:
    """Ungueltige modal_id wirft ValueError."""
    with pytest.raises(ValueError):
        Modal(modal_id="bad id", title="X", body="Y")
