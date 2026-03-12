"""Modal-Komponente fuer Dialog-Inhalte."""

from __future__ import annotations

import re

from pydantic import field_validator

from htmforge import Component
from htmforge.core.element import Child, Element
from htmforge.elements import button, div, h2


class Modal(Component):
    """Rendert ein dialogbasiertes Modal mit Header, Body und optionalem Footer."""

    modal_id: str
    title: str
    body: Child
    footer: Child | None = None
    close_label: str = "Schließen"

    def __init__(self, **data: object) -> None:
        """Validiert ``modal_id`` frueh, damit ungueltige IDs ValueError werfen."""
        modal_id = data.get("modal_id")
        if isinstance(modal_id, str) and not re.match(r"^[a-zA-Z0-9-]+$", modal_id):
            raise ValueError("modal_id darf nur a-z, A-Z, 0-9 und - enthalten")
        super().__init__(**data)

    @field_validator("modal_id")
    @classmethod
    def validate_modal_id(cls, value: str) -> str:
        """Erlaubt nur alphanumerische IDs mit Bindestrichen."""
        if not re.match(r"^[a-zA-Z0-9-]+$", value):
            raise ValueError("modal_id darf nur a-z, A-Z, 0-9 und - enthalten")
        return value

    def render(self) -> Element:
        """Erstellt das vollständige Modal-Markup mit Accessibility-Attributen."""
        title_id = f"{self.modal_id}__title"

        footer_element: Element | None = None
        if self.footer is not None:
            footer_element = div(self.footer, cls="modal__footer")

        return div(
            div(cls="modal__backdrop"),
            div(
                div(
                    h2(self.title, id=title_id, cls="modal__title"),
                    button("×", cls="modal__close", aria_label=self.close_label),
                    cls="modal__header",
                ),
                div(self.body, cls="modal__body"),
                footer_element,
                cls="modal__dialog",
            ),
            id=self.modal_id,
            cls="modal",
            role="dialog",
            aria_modal="true",
            aria_labelledby=title_id,
        )
