"""Formularelement-Komponente fuer htmforge.

Example:
    >>> from htmforge.components.form_field import FormField, InputType
    >>> field = FormField(name="email", label_text="E-Mail", input_type=InputType.EMAIL)
    >>> 'type="email"' in field.to_html()
    True
"""

from __future__ import annotations

from enum import StrEnum

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import div, input, label, textarea


class InputType(StrEnum):
    """Unterstuetzte ``<input>``-Typen."""

    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"  # noqa: S105
    NUMBER = "number"
    TEL = "tel"
    URL = "url"
    HIDDEN = "hidden"
    CHECKBOX = "checkbox"
    TEXTAREA = "textarea"


class FormField(Component):
    """Rendert ein beschriftetes Eingabefeld mit optionaler Fehleranzeige.

    ``InputType.TEXTAREA`` ist ein Sonderfall: hierfuer wird statt eines
    ``<input>`` ein ``<textarea>``-Element gerendert, dessen Inhalt ``value``
    ist (kein Attribut).

    Example:
        >>> from htmforge.components.form_field import FormField, InputType
        >>> field = FormField(
        ...     name="username",
        ...     label_text="Benutzername",
        ...     required=True,
        ... )
        >>> "required" in field.to_html()
        True
    """

    name: str
    label_text: str
    input_type: InputType = InputType.TEXT
    value: str = ""
    placeholder: str = ""
    required: bool = False
    error: str = ""
    field_id: str = ""
    min: int | float | None = None
    max: int | float | None = None

    def render(self) -> Element:
        """Erstellt ``div > label + input/textarea [+ div.field-error]``".

        ``InputType.HIDDEN`` ist ein Sonderfall: hier wird nur das
        ``<input type="hidden">`` ohne Label und Error-Div gerendert.
        """
        fid = self.field_id or self.name.replace(" ", "-")

        # Hidden inputs should not render a visible label or error container
        if self.input_type is InputType.HIDDEN:
            return self._render_control(fid)

        children: list[Element] = [
            label(
                self.label_text,
                for_=fid,
                aria_required="true" if self.required else None,
            ),
            self._render_control(fid),
        ]

        if self.error:
            children.append(div(self.error, cls="field-error"))

        return div(*children, cls=merge_cls(self.extra_cls))

    def _render_control(self, fid: str) -> Element:
        """Erstellt das eigentliche Eingabe-Element (``input`` oder ``textarea``)."""
        if self.input_type is InputType.TEXTAREA:
            return textarea(
                self.value or None,
                name=self.name,
                id=fid,
                placeholder=self.placeholder or None,
                required=True if self.required else None,
                aria_required="true" if self.required else None,
            )

        return input(
            type=self.input_type.value,
            name=self.name,
            id=fid,
            value=self.value or None,
            placeholder=self.placeholder or None,
            required=True if self.required else None,
            aria_required="true" if self.required else None,
            min=self.min,
            max=self.max,
        )
