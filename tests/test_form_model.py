"""Unit-Tests fuer htmforge.components.form_model (fields_from_model + Form.from_model)."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from htmforge.components import (
    CheckboxField,
    Form,
    FormField,
    SelectField,
    fields_from_model,
)
from htmforge.components.form_field import InputType


class Role(str, Enum):
    """Testweise Rolle als Enum."""

    ADMIN = "admin"
    USER = "user"


class UserData(BaseModel):
    """Beispiel-Model fuer die Introspektions-Tests."""

    name: str
    email: EmailStr
    age: int = Field(ge=18, le=120)
    bio: Optional[str] = None
    subscribe: bool = False
    role: Role = Role.USER


class TestFieldsFromModel:
    """Tests fuer ``fields_from_model()``."""

    def test_returns_one_component_per_field_in_order(self) -> None:
        components = fields_from_model(UserData)
        assert len(components) == 6

    def test_str_field_renders_text_input(self) -> None:
        field = fields_from_model(UserData)[0]
        assert isinstance(field, FormField)
        assert field.input_type is InputType.TEXT
        assert field.label_text == "Name"
        assert field.required is True

    def test_email_str_renders_email_input(self) -> None:
        field = fields_from_model(UserData)[1]
        assert isinstance(field, FormField)
        assert field.input_type is InputType.EMAIL

    def test_constrained_int_renders_number_with_bounds(self) -> None:
        field = fields_from_model(UserData)[2]
        assert isinstance(field, FormField)
        assert field.input_type is InputType.NUMBER
        assert field.min == 18
        assert field.max == 120

    def test_optional_str_renders_textarea(self) -> None:
        field = fields_from_model(UserData)[3]
        assert isinstance(field, FormField)
        assert field.input_type is InputType.TEXTAREA
        assert field.required is False

    def test_bool_renders_checkbox_field(self) -> None:
        field = fields_from_model(UserData)[4]
        assert isinstance(field, CheckboxField)
        assert field.checked is False

    def test_enum_renders_select_field(self) -> None:
        field = fields_from_model(UserData)[5]
        assert isinstance(field, SelectField)
        assert ("Admin", "admin") in field.options
        assert ("User", "user") in field.options
        assert field.selected == "user"

    def test_field_title_used_as_label_when_set(self) -> None:
        class Titled(BaseModel):
            full_name: str = Field(title="Vollständiger Name")

        field = fields_from_model(Titled)[0]
        assert field.label_text == "Vollständiger Name"

    def test_humanized_label_when_no_title(self) -> None:
        class Humanized(BaseModel):
            first_name: str

        field = fields_from_model(Humanized)[0]
        assert field.label_text == "First Name"

    def test_required_bool_field_defaults_to_unchecked(self) -> None:
        class RequiredBool(BaseModel):
            agree: bool

        field = fields_from_model(RequiredBool)[0]
        assert isinstance(field, CheckboxField)
        assert field.checked is False


class TestFormFromModel:
    """Tests fuer ``Form.from_model()``."""

    def test_returns_form_instance(self) -> None:
        form = Form.from_model(UserData)
        assert isinstance(form, Form)
        assert len(form.fields) == 6

    def test_default_action_is_empty_string(self) -> None:
        form = Form.from_model(UserData)
        assert form.action == ""

    def test_action_can_be_set(self) -> None:
        form = Form.from_model(UserData, action="/users")
        assert form.action == "/users"

    def test_extra_kwargs_forwarded_to_form(self) -> None:
        form = Form.from_model(UserData, action="/users", submit_label="Save")
        assert form.submit_label == "Save"

    def test_render_contains_all_fields(self) -> None:
        html = Form.from_model(UserData, action="/users").to_html()
        assert 'name="name"' in html
        assert 'name="email"' in html
        assert 'type="number"' in html
        assert "<textarea" in html
        assert 'type="checkbox"' in html
        assert "<select" in html

    def test_render_respects_number_bounds(self) -> None:
        html = Form.from_model(UserData, action="/users").to_html()
        assert 'min="18"' in html
        assert 'max="120"' in html