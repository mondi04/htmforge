"""Authentifizierungs-Helfer fuer htmforge (#25).

Stellt UI-Bausteine (``LoginForm``, ``LogoutButton``) und Render-Guards
(``requires_auth``, ``role_required``) fuer authentifizierte/rollenbasierte
Anzeige bereit. Der Auth-State (das ``user``-Objekt) wird vom umgebenden
Framework (FastAPI/Flask/Django) bereitgestellt — htmforge bleibt bewusst
auf die Praesentationsschicht beschraenkt und generiert/validiert keine
Tokens oder Sessions selbst.

Example:
    >>> from htmforge.auth import requires_auth
    >>> from htmforge.elements import div
    >>>
    >>> @requires_auth(fallback=div("Please log in"))
    ... def render_dashboard(user):
    ...     return div(f"Welcome, {user.name}")
    ...
    >>> render_dashboard(None).to_html()
    '<div>Please log in</div>'
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeVar

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import a, button, div, form, input, label
from htmforge.htmx import HxSwap

_R = TypeVar("_R", bound="Element | Component | None")


def _is_authenticated(user: Any) -> bool:  # noqa: ANN401
    """Prueft ob ``user`` einen eingeloggten Nutzer repraesentiert.

    Args:
        user: Das Nutzerobjekt (framework-spezifisch) oder ``None``.

    Returns:
        ``False`` wenn ``user`` ``None`` ist oder ``user.is_authenticated``
        explizit ``False`` ist (z.B. Django ``AnonymousUser``,
        Flask-Login), sonst ``True``.
    """
    if user is None:
        return False
    return bool(getattr(user, "is_authenticated", True))


def _has_role(user: Any, role: str) -> bool:  # noqa: ANN401
    """Prueft ob ``user`` die gegebene Rolle besitzt.

    Unterstuetzt sowohl ein iterierbares ``user.roles`` als auch ein
    einzelnes ``user.role``-Attribut, je nachdem was das Framework nutzt.

    Args:
        user: Das Nutzerobjekt.
        role: Die zu pruefende Rolle, z.B. ``"admin"``.

    Returns:
        ``True`` wenn die Rolle vorhanden ist.
    """
    roles = getattr(user, "roles", None)
    if roles is not None:
        return role in roles
    return getattr(user, "role", None) == role


def requires_auth(
    fallback: Element | Component | None = None,
) -> Callable[[Callable[..., _R]], Callable[..., Element | Component | None]]:
    """Decorator: rendert eine Funktion nur wenn ``user`` authentifiziert ist.

    Die dekorierte Funktion muss ``user`` als erstes Argument annehmen und
    ein :class:`~htmforge.core.element.Element` oder eine
    :class:`~htmforge.core.component.Component` zurueckgeben.

    Args:
        fallback: Was gerendert wird, wenn ``user`` nicht authentifiziert
            ist, default ``None`` (rendert nichts).

    Returns:
        Der Decorator.

    Example:
        >>> from htmforge.auth import requires_auth
        >>> from htmforge.elements import div
        >>> @requires_auth(fallback=div("Please log in"))
        ... def render_profile(user):
        ...     return div(user.name)
    """

    def decorator(
        fn: Callable[..., _R],
    ) -> Callable[..., Element | Component | None]:
        @functools.wraps(fn)
        def wrapper(
            user: Any,  # noqa: ANN401
            *args: Any,  # noqa: ANN401
            **kwargs: Any,  # noqa: ANN401
        ) -> Element | Component | None:
            if not _is_authenticated(user):
                return fallback
            return fn(user, *args, **kwargs)

        return wrapper

    return decorator


def role_required(
    role: str,
    fallback: Element | Component | None = None,
) -> Callable[[Callable[..., _R]], Callable[..., Element | Component | None]]:
    """Decorator: rendert eine Funktion nur wenn ``user`` die Rolle besitzt.

    Impliziert :func:`requires_auth` — ein nicht authentifizierter Nutzer
    faellt ebenfalls auf ``fallback`` zurueck.

    Args:
        role: Die erforderliche Rolle, z.B. ``"admin"``.
        fallback: Was gerendert wird, wenn die Rolle fehlt, default
            ``None``.

    Returns:
        Der Decorator.

    Example:
        >>> from htmforge.auth import role_required
        >>> from htmforge.elements import div
        >>> @role_required("admin", fallback=div("Forbidden"))
        ... def render_admin_panel(user):
        ...     return div("Secret controls")
    """

    def decorator(
        fn: Callable[..., _R],
    ) -> Callable[..., Element | Component | None]:
        @functools.wraps(fn)
        def wrapper(
            user: Any,  # noqa: ANN401
            *args: Any,  # noqa: ANN401
            **kwargs: Any,  # noqa: ANN401
        ) -> Element | Component | None:
            if not _is_authenticated(user) or not _has_role(user, role):
                return fallback
            return fn(user, *args, **kwargs)

        return wrapper

    return decorator


class LoginForm(Component):
    """Vorgefertigtes Login-Formular mit sicheren Autocomplete-Defaults.

    Rendert Benutzername/E-Mail- und Passwort-Felder mit
    ``autocomplete="username"``/``"email"`` bzw. ``"current-password"``,
    ARIA-Required-Attributen und optionalem "Forgot password?"-Link.

    Fields:
        action: str — form action URL
        method: str — HTTP-Methode, default "post"
        username_name: str — name-Attribut des Benutzername-Felds
        username_label: str — Beschriftung, default "Username"
        use_email: bool — wenn True: ``type="email"`` und
            ``autocomplete="email"`` statt ``"username"``
        password_name: str — name-Attribut des Passwort-Felds
        password_label: str — Beschriftung, default "Password"
        submit_label: str — Beschriftung des Submit-Buttons
        forgot_password_url: str — wenn gesetzt, wird ein Link gerendert
        forgot_password_label: str — Link-Text
        error: str — Fehlermeldung (z.B. "Invalid credentials")
        hx_post: str — optionale HTMX-POST-URL
        hx_target: str — HTMX-Ziel-Selektor
        hx_swap: HxSwap | None — HTMX-Swap-Strategie
    """

    action: str = ""
    method: str = "post"
    username_name: str = "username"
    username_label: str = "Username"
    use_email: bool = False
    password_name: str = "password"  # noqa: S105
    password_label: str = "Password"  # noqa: S105
    submit_label: str = "Log in"
    forgot_password_url: str = ""
    forgot_password_label: str = "Forgot password?"  # noqa: S105
    error: str = ""
    hx_post: str = ""
    hx_target: str = ""
    hx_swap: HxSwap | None = None

    def render(self) -> Element:
        """Erstellt das Login-Formular."""
        username_type = "email" if self.use_email else "text"
        username_autocomplete = "email" if self.use_email else "username"

        children: list[Element] = []
        if self.error:
            children.append(div(self.error, cls="login-form-error", role="alert"))

        children.append(
            div(
                label(self.username_label, for_="login-username"),
                input(
                    type=username_type,
                    name=self.username_name,
                    id="login-username",
                    autocomplete=username_autocomplete,
                    required=True,
                    aria_required="true",
                ),
                cls="field-wrapper",
            )
        )
        children.append(
            div(
                label(self.password_label, for_="login-password"),
                input(
                    type="password",  # noqa: S106
                    name=self.password_name,
                    id="login-password",
                    autocomplete="current-password",
                    required=True,
                    aria_required="true",
                ),
                cls="field-wrapper",
            )
        )

        if self.forgot_password_url:
            children.append(
                a(
                    self.forgot_password_label,
                    href=self.forgot_password_url,
                    cls="login-form-forgot",
                )
            )

        children.append(button(self.submit_label, type="submit"))

        form_attrs: dict[str, object] = {
            "action": self.action,
            "method": self.method,
            "cls": merge_cls("login-form", self.extra_cls),
        }
        if self.hx_post:
            form_attrs["hx_post"] = self.hx_post
        if self.hx_target:
            form_attrs["hx_target"] = self.hx_target
        if self.hx_swap:
            form_attrs["hx_swap"] = self.hx_swap

        return form(*children, **form_attrs)


class LogoutButton(Component):
    """Button, der einen POST-Request an eine Logout-URL sendet.

    Fields:
        logout_url: str — HTMX-POST-Ziel
        label: str — Button-Beschriftung, default "Log out"
        confirm: str — wenn gesetzt, wird ``hx-confirm`` gerendert
        hx_target: str — HTMX-Ziel-Selektor
        hx_swap: HxSwap | None — HTMX-Swap-Strategie
    """

    logout_url: str
    label: str = "Log out"
    confirm: str = ""
    hx_target: str = ""
    hx_swap: HxSwap | None = None

    def render(self) -> Element:
        """Erstellt den Logout-Button."""
        attrs: dict[str, object] = {
            "type": "button",
            "cls": merge_cls("logout-button", self.extra_cls),
            "hx_post": self.logout_url,
        }
        if self.confirm:
            attrs["hx_confirm"] = self.confirm
        if self.hx_target:
            attrs["hx_target"] = self.hx_target
        if self.hx_swap:
            attrs["hx_swap"] = self.hx_swap
        return button(self.label, **attrs)


__all__ = [
    "LoginForm",
    "LogoutButton",
    "requires_auth",
    "role_required",
]
