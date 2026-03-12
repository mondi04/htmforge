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
from htmforge.core.element import Element
from htmforge.elements import div, input, label


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


class FormField(Component):
    """Rendert ein beschriftetes Eingabefeld mit optionaler Fehleranzeige.

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

    def render(self) -> Element:
        """Erstellt ``div > label + input [+ div.field-error]``."""
        fid = self.field_id or self.name.replace(" ", "-")

        children: list[Element] = [
            label(
                self.label_text,
                for_=fid,
                aria_required="true" if self.required else None,
            ),
            input(
                type=self.input_type.value,
                name=self.name,
                id=fid,
                value=self.value or None,
                placeholder=self.placeholder or None,
                required=True if self.required else None,
                aria_required="true" if self.required else None,
            ),
        ]

        if self.error:
            children.append(div(self.error, cls="field-error"))

        return div(*children)
