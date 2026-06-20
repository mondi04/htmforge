"""Forms-System fuer htmforge.

Provides Form, SelectField, CheckboxField, RadioGroup, FormGroup
with optional validation error dict integration.

Example:
    >>> from htmforge.components.forms import Form, SelectField
    >>> form = Form(
    ...     action="/submit",
    ...     method="post",
    ...     fields=[SelectField(name="role", options=[("Admin","admin")])],
    ... )
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import (
    button,
    div,
    fieldset,
    form,
    input,
    label,
    legend,
    option,
    select,
)
from htmforge.htmx import HxSwap


class SelectField(Component):
    """Dropdown-Auswahlliste mit typisierten Optionen.

    Fields:
        name: str — name-Attribut des select
        options: list[tuple[str, str]] — (label, value) Paare
        selected: str — aktuell ausgewählter value
        label_text: str — Beschriftung über dem Select
        required: bool — Pflichtfeld
        error: str — Fehlermeldung (rendert div.field-error)
        field_id: str — HTML id, default = name
    """

    name: str
    options: list[tuple[str, str]]
    selected: str = ""
    label_text: str = ""
    required: bool = False
    error: str = ""
    field_id: str = ""

    def render(self) -> Element:
        """Rendert ein beschriftetes select-Element."""
        fid = self.field_id or self.name
        children: list[Element] = []
        if self.label_text:
            children.append(label(self.label_text, for_=fid))
        opts = [
            option(
                lbl,
                value=val,
                selected=True if val == self.selected else None,
            )
            for lbl, val in self.options
        ]
        sel = select(
            *opts,
            name=self.name,
            id=fid,
            required=True if self.required else None,
        )
        children.append(sel)
        if self.error:
            children.append(div(self.error, cls="field-error"))
        return div(*children, cls=merge_cls("field-wrapper", self.extra_cls))


class CheckboxField(Component):
    """Einzelne Checkbox mit Label.

    Fields:
        name: str — name-Attribut
        label_text: str — Beschriftung neben der Checkbox
        checked: bool — Vorausgewählt
        value: str — value-Attribut, default "1"
        required: bool — Pflichtfeld
        error: str — Fehlermeldung
        field_id: str — HTML id, default = name
    """

    name: str
    label_text: str
    checked: bool = False
    value: str = "1"
    required: bool = False
    error: str = ""
    field_id: str = ""

    def render(self) -> Element:
        """Rendert eine Checkbox mit Label."""
        fid = self.field_id or self.name
        children: list[Element] = [
            input(
                type="checkbox",
                name=self.name,
                id=fid,
                value=self.value,
                checked=True if self.checked else None,
                required=True if self.required else None,
            ),
            label(self.label_text, for_=fid),
        ]
        if self.error:
            children.append(div(self.error, cls="field-error"))
        return div(*children, cls=merge_cls("checkbox-field", self.extra_cls))


class RadioGroup(Component):
    """Gruppe von Radio-Buttons aus einer Options-Liste.

    Fields:
        name: str — gemeinsames name-Attribut aller Radios
        options: list[tuple[str, str]] — (label, value) Paare
        selected: str — aktuell ausgewählter value
        legend_text: str — Gruppenbezeichnung im fieldset
        required: bool — Pflichtfeld auf erstem Radio
        error: str — Fehlermeldung
    """

    name: str
    options: list[tuple[str, str]]
    selected: str = ""
    legend_text: str = ""
    required: bool = False
    error: str = ""

    def render(self) -> Element:
        """Rendert eine Gruppe von Radio-Buttons im Fieldset."""
        children: list[Element] = []
        if self.legend_text:
            children.append(legend(self.legend_text))

        for i, (lbl, val) in enumerate(self.options):
            radio_id = f"{self.name}-{val}"
            is_first = i == 0
            children.append(
                div(
                    input(
                        type="radio",
                        name=self.name,
                        id=radio_id,
                        value=val,
                        checked=True if val == self.selected else None,
                        required=True if self.required and is_first else None,
                    ),
                    label(lbl, for_=radio_id),
                    cls="radio-item",
                )
            )

        if self.error:
            children.append(div(self.error, cls="field-error"))

        return fieldset(*children, cls=merge_cls("radiogroup", self.extra_cls))


class FormGroup(Component):
    """Layout-Container fuer mehrere Formularfelder.

    Fields:
        fields: list[Component] — Felder die gerendert werden
        legend_text: str — optionale Gruppenbezeichnung
        group_cls: str — extra CSS-Klasse auf dem wrapper div
    """

    fields: list[Component]
    legend_text: str = ""
    group_cls: str = ""

    def render(self) -> Element:
        """Rendert eine Feldgruppe mit optionaler Legend."""
        children: list[Element] = []
        if self.legend_text:
            children.append(div(self.legend_text, cls="form-group-legend"))

        for field in self.fields:
            children.append(field.render())

        return div(
            *children,
            cls=merge_cls("form-group", self.group_cls, self.extra_cls),
        )


class Form(Component):
    """Formular-Container mit HTMX-Submit-Unterstuetzung.

    Fields:
        action: str — form action URL, default "" (z.B. wenn nur hx_post
          genutzt wird, oder bei automatisch erzeugten Formularen via
          Form.from_model())
        method: str — "get" or "post", default "post"
        fields: list[Component] — Formularfelder
        submit_label: str — Beschriftung des Submit-Buttons, default "Absenden"
        errors: dict[str, str] — Validierungsfehler {field_name: message}
          Wenn gesetzt, werden Fehler automatisch an passende Felder
          weitergegeben.
        hx_post: str — HTMX POST URL (optional, overrides action for HTMX)
        hx_target: str — HTMX target selector
        hx_swap: HxSwap | None — HTMX swap strategy
    """

    action: str = ""
    method: str = "post"
    fields: list[Component] = []
    submit_label: str = "Absenden"
    errors: dict[str, str] = {}
    hx_post: str = ""
    hx_target: str = ""
    hx_swap: HxSwap | None = None

    @classmethod
    def from_model(
        cls,
        model: type[BaseModel],
        action: str = "",
        **kwargs: Any,  # noqa: ANN401
    ) -> Form:
        """Erzeugt ein ``Form`` automatisch aus einem Pydantic-Model.

        Jedes Modellfeld wird ueber
        :func:`htmforge.components.form_model.fields_from_model` in eine
        passende Formularkomponente uebersetzt (``FormField``,
        ``CheckboxField`` oder ``SelectField``) — inklusive Pflichtfeld- und
        Min/Max-Constraints, soweit aus dem Pydantic-Feld ableitbar.

        Args:
            model: Eine Pydantic ``BaseModel``-Subklasse.
            action: Form-Action-URL, default "".
            **kwargs: Weitere ``Form``-Props (``method``, ``submit_label``,
                ``errors``, ``hx_post``, ``hx_target``, ``hx_swap``, ...).
                ``fields`` darf hier nicht gesetzt werden, da es automatisch
                generiert wird.

        Returns:
            Eine neue ``Form``-Instanz mit automatisch generierten Feldern.

        Example:
            >>> from pydantic import BaseModel, EmailStr, Field
            >>> class UserData(BaseModel):
            ...     name: str
            ...     email: EmailStr
            ...     age: int = Field(ge=18, le=120)
            ...
            >>> form = Form.from_model(UserData, action="/users")
        """
        # Lazy import: form_model.py importiert CheckboxField/SelectField aus
        # diesem Modul — ein Import auf Modulebene wuerde einen Zirkelimport
        # erzeugen.
        from htmforge.components.form_model import fields_from_model

        return cls(action=action, fields=fields_from_model(model), **kwargs)

    def render(self) -> Element:
        """Rendert das Formular mit auto-error-Injection."""
        # Apply errors to matching fields
        rendered_fields: list[Element] = []
        for field in self.fields:
            field_to_render = field
            # Check if field has a 'name' attribute and matching error
            if hasattr(field, "name") and hasattr(field, "error"):
                field_name = field.name
                if field_name in self.errors:
                    # Clone field with error
                    field_to_render = field.clone(error=self.errors[field_name])
            rendered_fields.append(field_to_render.render())

        # Build form attributes
        form_attrs: dict[str, object] = {
            "action": self.action,
            "method": self.method,
            "cls": merge_cls("form", self.extra_cls),
        }
        if self.hx_post:
            form_attrs["hx_post"] = self.hx_post
        if self.hx_target:
            form_attrs["hx_target"] = self.hx_target
        if self.hx_swap:
            form_attrs["hx_swap"] = self.hx_swap

        # Build form content
        form_children: list[Element] = rendered_fields + [
            button(self.submit_label, type="submit")
        ]

        return form(*form_children, **form_attrs)
