"""Tests fuer Framework-Adapter to_flask() und to_django().

Flask und Django werden per pytest.importorskip automatisch
uebersprungen wenn sie nicht installiert sind.
"""

from __future__ import annotations

import sys

import pytest

from htmforge import Component
from htmforge.components import Alert, Badge, BadgeVariant
from htmforge.core.element import Element
from htmforge.elements import div, p


class SimpleCard(Component):
    """Minimale Test-Komponente."""

    title: str

    def render(self) -> Element:
        return div(p(self.title))


class TestFlaskAdapter:
    """Tests fuer Component.to_flask()."""

    def test_to_flask_returns_flask_response(self) -> None:
        flask = pytest.importorskip("flask")
        card = SimpleCard(title="Hello")
        response = card.to_flask()
        assert isinstance(response, flask.Response)

    def test_to_flask_content_type_is_html(self) -> None:
        pytest.importorskip("flask")
        card = SimpleCard(title="Hello")
        response = card.to_flask()
        assert "text/html" in response.content_type

    def test_to_flask_body_contains_rendered_html(self) -> None:
        pytest.importorskip("flask")
        card = SimpleCard(title="Flask Test")
        response = card.to_flask()
        assert b"Flask Test" in response.data

    def test_alert_to_flask(self) -> None:
        flask = pytest.importorskip("flask")
        alert = Alert(message="OK")
        response = alert.to_flask()
        assert isinstance(response, flask.Response)
        assert b"OK" in response.data

    def test_badge_to_flask(self) -> None:
        pytest.importorskip("flask")
        badge = Badge(text="New", variant=BadgeVariant.SUCCESS)
        response = badge.to_flask()
        assert b"New" in response.data

    def test_to_flask_raises_import_error_without_flask(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pytest.importorskip("flask")
        monkeypatch.setitem(sys.modules, "flask", None)
        card = SimpleCard(title="Test")
        with pytest.raises(ImportError):
            card.to_flask()


class TestDjangoAdapter:
    """Tests fuer Component.to_django()."""

    def test_to_django_returns_http_response(self) -> None:
        django_http = pytest.importorskip("django.http")
        card = SimpleCard(title="Hello")
        response = card.to_django()
        assert isinstance(response, django_http.HttpResponse)

    def test_to_django_content_type_is_html(self) -> None:
        pytest.importorskip("django.http")
        card = SimpleCard(title="Hello")
        response = card.to_django()
        assert "text/html" in response.get("Content-Type", "")

    def test_to_django_body_contains_rendered_html(self) -> None:
        pytest.importorskip("django.http")
        card = SimpleCard(title="Django Test")
        response = card.to_django()
        assert b"Django Test" in response.content

    def test_alert_to_django(self) -> None:
        django_http = pytest.importorskip("django.http")
        alert = Alert(message="Info")
        response = alert.to_django()
        assert isinstance(response, django_http.HttpResponse)

    def test_to_django_raises_import_error_without_django(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pytest.importorskip("django")
        monkeypatch.setitem(sys.modules, "django.http", None)
        monkeypatch.setitem(sys.modules, "django", None)
        card = SimpleCard(title="Test")
        with pytest.raises(ImportError):
            card.to_django()


class TestFastAPIAdapter:
    """Tests fuer Component.to_fastapi()."""

    def test_to_fastapi_returns_html_response(self) -> None:
        fastapi_responses = pytest.importorskip("fastapi.responses")
        card = SimpleCard(title="Hello")
        response = card.to_fastapi()
        assert isinstance(response, fastapi_responses.HTMLResponse)

    def test_to_fastapi_body_contains_rendered_html(self) -> None:
        pytest.importorskip("fastapi")
        card = SimpleCard(title="FastAPI Test")
        response = card.to_fastapi()
        assert b"FastAPI Test" in response.body

    def test_to_fastapi_raises_import_error_without_fastapi(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pytest.importorskip("fastapi")
        monkeypatch.setitem(sys.modules, "fastapi", None)
        monkeypatch.setitem(sys.modules, "fastapi.responses", None)
        card = SimpleCard(title="Test")
        with pytest.raises(ImportError):
            card.to_fastapi()
