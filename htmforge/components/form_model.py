"""Pydantic-Model-Introspektion fuer Form.from_model().

Wandelt Pydantic v2 FieldInfo-Objekte automatisch in passende
htmforge-Formularfelder um (FormField, CheckboxField, SelectField).
"""

from __future__ import annotations

from enum import Enum
from typing import Union, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from htmforge import Component
from htmforge.components.form_field import FormField, InputType
from htmforge.components.forms import CheckboxField, SelectField


def _unwrap_optional(annotation: object) -> tuple[object, bool]:
    """Entpackt Optional[X] zu (X, True); gibt (annotation, False) sonst zurück."""
    if get_origin(annotation) is Union:
        args = [a for a in get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return args[0], True
    return annotation, False


def _humanize(field_name: str) -> str:
    """Wandelt 'subscribe_news' in 'Subscribe News' um."""
    return field_name.replace("_", " ").title()


def _numeric_bounds(field_info: FieldInfo) -> tuple[float | None, float | None]:
    """Extrahiert min/max aus Ge/Gt/Le/Lt-Constraints, falls vorhanden."""
    min_val: float | None = None
    max_val: float | None = None
    for meta in field_info.metadata:
        if hasattr(meta, "ge"):
            min_val = meta.ge
        elif hasattr(meta, "gt"):
            min_val = meta.gt
        elif hasattr(meta, "le"):
            max_val = meta.le
        elif hasattr(meta, "lt"):
            max_val = meta.lt
    return min_val, max_val


def field_to_component(name: str, field_info: FieldInfo) -> Component:
    """Wandelt ein einzelnes Pydantic-Feld in eine htmforge-Formularkomponente um."""
    annotation, is_optional = _unwrap_optional(field_info.annotation)
    required = field_info.is_required()
    label_text = field_info.title or _humanize(name)

    # bool -> Checkbox
    if annotation is bool:
        checked = bool(field_info.default) if not field_info.is_required() else False
        return CheckboxField(
            name=name,
            label_text=label_text,
            checked=checked,
            required=required,
        )

    # Enum -> SelectField
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        options = [(member.name.replace("_", " ").title(), str(member.value)) for member in annotation]
        default_val = (
            str(field_info.default.value)
            if isinstance(field_info.default, Enum)
            else ""
        )
        return SelectField(
            name=name,
            label_text=label_text,
            options=options,
            selected=default_val,
            required=required,
        )

    # int/float -> NUMBER, mit Constraints falls vorhanden
    if annotation in (int, float):
        min_val, max_val = _numeric_bounds(field_info)
        return FormField(
            name=name,
            label_text=label_text,
            input_type=InputType.NUMBER,
            required=required,
            min=min_val,
            max=max_val,
        )

    # Optional[str] -> Textarea (langer, optionaler Freitext laut Issue-Vorgabe)
    if annotation is str and is_optional:
        return FormField(
            name=name,
            label_text=label_text,
            input_type=InputType.TEXTAREA,
            required=required,
        )

    # str mit EmailStr-Erkennung am Klassennamen (kein Import von EmailStr nötig,
    # damit das optionale pydantic[email]-Extra keine harte Abhängigkeit wird)
    type_name = getattr(annotation, "__name__", "")
    if type_name == "EmailStr":
        return FormField(
            name=name,
            label_text=label_text,
            input_type=InputType.EMAIL,
            required=required,
        )

    # Fallback: einfacher Text
    return FormField(
        name=name,
        label_text=label_text,
        input_type=InputType.TEXT,
        required=required,
    )


def fields_from_model(model: type[BaseModel]) -> list[Component]:
    """Erzeugt eine Liste von htmforge-Formularkomponenten aus einem Pydantic-Model.

    Args:
        model: Eine Pydantic ``BaseModel``-Subklasse.

    Returns:
        Liste von Component-Instanzen, eine pro Modellfeld, in Deklarationsreihenfolge.
    """
    return [
        field_to_component(name, field_info)
        for name, field_info in model.model_fields.items()
    ]