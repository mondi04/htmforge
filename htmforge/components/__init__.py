"""Vorgefertigte, wiederverwendbare Komponenten fuer htmforge."""

from .accordion import Accordion
from .alert import Alert, AlertVariant
from .badge import Badge, BadgeVariant
from .behavioral import AutocompleteInput, InfiniteScrollList, InlineEditor
from .breadcrumb import Breadcrumb
from .dashboard import DashboardLayout, Widget
from .dropdown import Dropdown
from .form_field import FormField, InputType
from .form_model import fields_from_model
from .forms import (
    CheckboxField,
    Form,
    FormGroup,
    RadioGroup,
    SelectField,
)
from .modal import Modal
from .pagination import Pagination
from .search_input import SearchInput
from .spinner import Spinner, SpinnerSize
from .table import ColumnDef, DataTable
from .tabs import Tabs
from .toast import Toast, ToastVariant

__all__ = [
    "Accordion",
    "Alert",
    "AlertVariant",
    "AutocompleteInput",
    "Badge",
    "BadgeVariant",
    "Breadcrumb",
    "CheckboxField",
    "ColumnDef",
    "DashboardLayout",
    "DataTable",
    "Dropdown",
    "Form",
    "FormField",
    "FormGroup",
    "InfiniteScrollList",
    "InlineEditor",
    "InputType",
    "Modal",
    "Pagination",
    "RadioGroup",
    "SearchInput",
    "SelectField",
    "Spinner",
    "SpinnerSize",
    "Tabs",
    "Toast",
    "ToastVariant",
    "Widget",
    "fields_from_model",
]
