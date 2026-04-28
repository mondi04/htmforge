"""Modal-Dialog-Komponente mit HTMX-Content-Loading.

Example:
    >>> from htmforge.components import Modal
    >>> m = Modal(
    ...     modal_id="confirm",
    ...     trigger_label="Öffnen",
    ...     hx_url="/modal/content",
    ...     hx_target="#confirm-body",
    ... )
    >>> "hx-get" in m.to_html()
    True
"""

from __future__ import annotations

from htmforge import Component
from htmforge.core.element import Element
from htmforge.elements import button, dialog, div, form, raw
from htmforge.htmx import HxSwap


class Modal(Component):
    """Trigger-Button + leeres Dialog-Overlay, Inhalt wird per HTMX geladen.

    Renders:
        <div class="modal-wrapper">
          <button hx-get=hx_url hx-target="#modal_id-body" hx-swap="innerHTML"
                  onclick="document.getElementById('modal_id').showModal()">
            trigger_label
          </button>
          <dialog id=modal_id class="modal">
            <div id="modal_id-body" class="modal-body"></div>
            <form method="dialog">
              <button class="modal-close">Schließen</button>
            </form>
          </dialog>
        </div>

    Fields:
        modal_id: str — unique HTML id for the <dialog>
        trigger_label: str — label on the trigger button
        hx_url: str — URL to load modal content from
        hx_target: str = "" — overrides default target if set
        close_label: str = "Schließen"
    """

    modal_id: str
    trigger_label: str
    hx_url: str
    hx_target: str = ""
    close_label: str = "Schließen"

    def render(self) -> Element:
        """Erstellt den Trigger-Button und das ``<dialog>``-Overlay."""
        body_id = f"{self.modal_id}-body"
        target = self.hx_target or f"#{body_id}"

        return div(
            button(
                self.trigger_label,
                type="button",
                data_modal_target=self.modal_id,
                cls="modal-trigger",
                hx_get=self.hx_url,
                hx_target=target,
                hx_swap=HxSwap.INNER_HTML,
            ),
            dialog(
                div(id=body_id, cls="modal-body"),
                form(
                    button(self.close_label, cls="modal-close"),
                    method="dialog",
                ),
                id=self.modal_id,
                cls="modal",
            ),
            raw(
                "<script>"
                "document.querySelectorAll('[data-modal-target]').forEach(function(btn){"
                "btn.addEventListener('click',function(){"
                "var id=btn.getAttribute('data-modal-target');"
                "var dlg=document.getElementById(id);"
                "if(dlg)dlg.showModal();"
                "});"
                "});"
                "</script>"
            ),
            cls="modal-wrapper",
        )
