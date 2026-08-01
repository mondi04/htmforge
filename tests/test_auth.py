"""Tests fuer ``htmforge.auth`` (#25)."""

from __future__ import annotations

from dataclasses import dataclass, field

from htmforge.auth import LoginForm, LogoutButton, requires_auth, role_required
from htmforge.core.element import Element
from htmforge.elements import div


@dataclass
class FakeUser:
    """Minimales Test-Double fuer ein Framework-User-Objekt."""

    name: str
    is_authenticated: bool = True
    roles: list[str] = field(default_factory=list)


class TestRequiresAuth:
    """Tests fuer den ``requires_auth``-Decorator."""

    def test_renders_wrapped_function_when_authenticated(self) -> None:
        """Authentifizierter User: die dekorierte Funktion wird gerendert."""

        @requires_auth(fallback=div("Please log in"))
        def render_profile(user: FakeUser) -> Element:
            return div(f"Hi {user.name}")

        result = render_profile(FakeUser(name="Ada"))
        assert result is not None
        assert result.to_html() == "<div>Hi Ada</div>"

    def test_renders_fallback_when_user_is_none(self) -> None:
        """Kein User: fallback wird gerendert."""

        @requires_auth(fallback=div("Please log in"))
        def render_profile(user: FakeUser | None) -> Element:
            return div("secret")

        result = render_profile(None)
        assert result is not None
        assert result.to_html() == "<div>Please log in</div>"

    def test_renders_fallback_when_not_authenticated(self) -> None:
        """user.is_authenticated=False: fallback wird gerendert."""

        @requires_auth(fallback=div("Please log in"))
        def render_profile(user: FakeUser) -> Element:
            return div("secret")

        anon = FakeUser(name="Anon", is_authenticated=False)
        result = render_profile(anon)
        assert result is not None
        assert result.to_html() == "<div>Please log in</div>"

    def test_default_fallback_is_none(self) -> None:
        """Ohne fallback wird None zurueckgegeben."""

        @requires_auth()
        def render_profile(user: FakeUser) -> Element:
            return div("secret")

        assert render_profile(None) is None


class TestRoleRequired:
    """Tests fuer den ``role_required``-Decorator."""

    def test_renders_when_role_present(self) -> None:
        """User mit passender Rolle: Funktion wird gerendert."""

        @role_required("admin", fallback=div("Forbidden"))
        def render_admin_panel(user: FakeUser) -> Element:
            return div("controls")

        admin = FakeUser(name="Ada", roles=["admin"])
        result = render_admin_panel(admin)
        assert result is not None
        assert result.to_html() == "<div>controls</div>"

    def test_renders_fallback_when_role_missing(self) -> None:
        """User ohne passende Rolle: fallback wird gerendert."""

        @role_required("admin", fallback=div("Forbidden"))
        def render_admin_panel(user: FakeUser) -> Element:
            return div("controls")

        member = FakeUser(name="Grace", roles=["member"])
        result = render_admin_panel(member)
        assert result is not None
        assert result.to_html() == "<div>Forbidden</div>"

    def test_renders_fallback_when_unauthenticated(self) -> None:
        """Nicht authentifizierter User faellt ebenfalls auf fallback zurueck."""

        @role_required("admin", fallback=div("Forbidden"))
        def render_admin_panel(user: FakeUser) -> Element:
            return div("controls")

        assert render_admin_panel(None) is not None
        result = render_admin_panel(None)
        assert result is not None
        assert result.to_html() == "<div>Forbidden</div>"


class TestLoginForm:
    """Tests fuer die ``LoginForm``-Komponente."""

    def test_username_field_has_username_autocomplete(self) -> None:
        """Default: autocomplete='username' und type='text'."""
        html = LoginForm(action="/login").to_html()
        assert 'autocomplete="username"' in html
        assert 'type="text"' in html

    def test_use_email_switches_type_and_autocomplete(self) -> None:
        """use_email=True setzt type='email' und autocomplete='email'."""
        html = LoginForm(action="/login", use_email=True).to_html()
        assert 'type="email"' in html
        assert 'autocomplete="email"' in html

    def test_password_field_has_current_password_autocomplete(self) -> None:
        """Passwortfeld hat autocomplete='current-password'."""
        html = LoginForm(action="/login").to_html()
        assert 'type="password"' in html
        assert 'autocomplete="current-password"' in html

    def test_forgot_password_link_rendered_when_url_set(self) -> None:
        """Forgot-password-Link wird nur bei gesetzter URL gerendert."""
        html = LoginForm(action="/login", forgot_password_url="/reset").to_html()
        assert 'href="/reset"' in html
        assert "Forgot password?" in html

    def test_no_forgot_password_link_by_default(self) -> None:
        """Ohne forgot_password_url wird kein Link gerendert."""
        html = LoginForm(action="/login").to_html()
        assert "Forgot password?" not in html

    def test_error_rendered_with_alert_role(self) -> None:
        """error wird mit role='alert' gerendert."""
        html = LoginForm(action="/login", error="Invalid credentials").to_html()
        assert 'role="alert"' in html
        assert "Invalid credentials" in html

    def test_hx_post_sets_htmx_attributes(self) -> None:
        """hx_post wird als hx-post-Attribut auf dem form-Tag gerendert."""
        html = LoginForm(hx_post="/login", hx_target="#result").to_html()
        assert 'hx-post="/login"' in html
        assert 'hx-target="#result"' in html


class TestLogoutButton:
    """Tests fuer die ``LogoutButton``-Komponente."""

    def test_renders_button_with_hx_post(self) -> None:
        """Button rendert hx-post auf logout_url."""
        html = LogoutButton(logout_url="/logout").to_html()
        assert 'hx-post="/logout"' in html
        assert "Log out" in html

    def test_custom_label(self) -> None:
        """Benutzerdefiniertes Label wird gerendert."""
        html = LogoutButton(logout_url="/logout", label="Sign out").to_html()
        assert "Sign out" in html

    def test_confirm_sets_hx_confirm(self) -> None:
        """confirm setzt hx-confirm."""
        html = LogoutButton(logout_url="/logout", confirm="Are you sure?").to_html()
        assert 'hx-confirm="Are you sure?"' in html

    def test_no_confirm_by_default(self) -> None:
        """Ohne confirm wird kein hx-confirm gerendert."""
        html = LogoutButton(logout_url="/logout").to_html()
        assert "hx-confirm" not in html
