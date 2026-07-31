"""Behavioral-Affordance-Komponenten fuer haeufige HTMX-Interaktionsmuster (#26).

Buendelt drei High-Level-Komponenten, die wiederkehrende UX-Patterns
(Autocomplete-Suche, Infinite Scroll, Inline-Editing) mit sinnvollen
HTMX-Defaults und ARIA-Attributen kapseln, statt hx-get/hx-trigger/hx-target
und Edge-Cases (Debounce, Race-Konditionen, leere Ergebnisse) manuell pro
Projekt neu zu verdrahten.
"""

from __future__ import annotations

from typing import Literal

from htmforge import Component
from htmforge.core.element import Element, merge_cls
from htmforge.elements import (
    button,
    div,
    form,
    input,
    li,
    option,
    raw,
    select,
    span,
    textarea,
    ul,
)
from htmforge.htmx import HxSwap, HxTrigger


class AutocompleteInput(Component):
    """Text-Input mit HTMX-Debounce-Suche und ARIA-Combobox-Listbox.

    Rendert ein Text-Input plus eine leere Ergebnis-Listbox, die per HTMX
    nachgeladen wird, sobald mindestens ``min_chars`` Zeichen eingegeben
    wurden. Ein einmalig registrierter, dokumentweiter Skript-Block (analog
    zum Fix in #16) erlaubt Pfeiltasten-Navigation ueber die vom Server
    gelieferten ``<li role="option">``-Eintraege sowie Auswahl per Enter.

    Fields:
        name: str — name-Attribut des Inputs
        search_url: str — HTMX-URL, die Vorschlaege liefert (hx-get)
        placeholder: str = ""
        min_chars: int — Mindestanzahl Zeichen bevor gesucht wird, default 2
        debounce_ms: int — Debounce-Verzoegerung, default 300
        input_id: str — HTML-id des Inputs, default = name
        indicator: str — optionaler hx-indicator-Selektor
    """

    name: str
    search_url: str
    placeholder: str = ""
    min_chars: int = 2
    debounce_ms: int = 300
    input_id: str = ""
    indicator: str = ""

    def render(self) -> Element:
        """Erstellt Input + Listbox mit Debounce- und Mindestlaenge-Trigger."""
        iid = self.input_id or self.name
        listbox_id = f"{iid}-listbox"
        trigger = (
            f"keyup[target.value.length>={self.min_chars}] changed "
            f"delay:{self.debounce_ms}ms"
        )

        return div(
            input(
                type="text",
                name=self.name,
                id=iid,
                placeholder=self.placeholder or None,
                autocomplete="off",
                role="combobox",
                aria_expanded="false",
                aria_autocomplete="list",
                aria_controls=listbox_id,
                data_autocomplete_input="true",
                hx_get=self.search_url,
                hx_trigger=trigger,
                hx_target=f"#{listbox_id}",
                hx_swap=HxSwap.INNER_HTML,
                hx_indicator=self.indicator or None,
            ),
            ul(
                id=listbox_id,
                role="listbox",
                cls="autocomplete-list",
            ),
            _AUTOCOMPLETE_SCRIPT,
            cls=merge_cls("autocomplete-wrapper", self.extra_cls),
        )


_AUTOCOMPLETE_SCRIPT = raw(
    "<script>"
    "if(!window.__htmforgeAutocompleteDelegated){"
    "window.__htmforgeAutocompleteDelegated=true;"
    "document.addEventListener('keydown',function(e){"
    "var input=e.target;"
    "if(!input.matches('[data-autocomplete-input]'))return;"
    "var list=document.getElementById(input.getAttribute('aria-controls'));"
    "if(!list)return;"
    "var opts=Array.prototype.slice.call(list.querySelectorAll('[role=\"option\"]'));"
    "if(!opts.length)return;"
    "var active=list.querySelector('[aria-selected=\"true\"]');"
    "var idx=opts.indexOf(active);"
    "if(e.key==='ArrowDown'||e.key==='ArrowUp'){"
    "e.preventDefault();"
    "if(active)active.removeAttribute('aria-selected');"
    "idx=e.key==='ArrowDown'?(idx+1)%opts.length:(idx-1+opts.length)%opts.length;"
    "opts[idx].setAttribute('aria-selected','true');"
    "input.setAttribute('aria-activedescendant',opts[idx].id||'');"
    "}else if(e.key==='Enter'&&active){"
    "e.preventDefault();"
    "active.click();"
    "}else if(e.key==='Escape'){"
    "list.replaceChildren();"
    "input.removeAttribute('aria-activedescendant');"
    "}"
    "});"
    "}"
    "</script>"
)


class InfiniteScrollList(Component):
    """Container-Liste, die per HTMX automatisch weitere Seiten nachlaedt.

    Das letzte Kind ist ein unsichtbares Sentinel-Element mit
    ``hx-trigger="revealed"`` (oder ``intersect``): sobald es in den
    sichtbaren Bereich gescrollt wird, laedt HTMX ``next_page_url`` nach und
    ersetzt das Sentinel per ``outerHTML``-Swap. Der Server-Response fuer
    diese Seite muss die naechste Charge Items plus (falls vorhanden) ein
    neues Sentinel-Element enthalten — ist keine weitere Seite vorhanden,
    liefert der Endpunkt einfach keinen neuen Sentinel und das Nachladen
    stoppt von selbst.

    Fields:
        items: list[Element | Component | str] — initial gerenderte Items
        next_page_url: str | None — HTMX-URL fuer die naechste Seite, None
            = kein Sentinel (z.B. letzte Seite bereits erreicht)
        list_id: str — HTML-id des Containers, default "infinite-scroll-list"
        trigger: HxTrigger — Ladeausloeser, default ``HxTrigger.REVEALED``
        item_cls: str — CSS-Klasse pro Item-Wrapper
        indicator: str — optionaler hx-indicator-Selektor
    """

    items: list[Element | Component | str] = []
    next_page_url: str | None = None
    list_id: str = "infinite-scroll-list"
    trigger: HxTrigger = HxTrigger.REVEALED
    item_cls: str = ""
    indicator: str = ""

    def render(self) -> Element:
        """Erstellt die Item-Liste mit optionalem Nachlade-Sentinel."""
        children: list[Element] = [
            li(item, cls=merge_cls("infinite-scroll-item", self.item_cls))
            for item in self.items
        ]

        if self.next_page_url:
            sentinel_id = f"{self.list_id}-sentinel"
            children.append(
                li(
                    id=sentinel_id,
                    cls="infinite-scroll-sentinel",
                    hx_get=self.next_page_url,
                    hx_trigger=self.trigger,
                    hx_target=f"#{sentinel_id}",
                    hx_swap=HxSwap.OUTER_HTML,
                    hx_indicator=self.indicator or None,
                )
            )

        return ul(
            *children,
            id=self.list_id,
            cls=merge_cls("infinite-scroll-list", self.extra_cls),
        )


class InlineEditor(Component):
    """Macht einen Wert per Klick editierbar; speichert Aenderungen via HTMX.

    Rendert sowohl die Anzeige (``span``) als auch ein vorab gerendertes,
    per CSS verstecktes Bearbeitungsformular im selben Wrapper — ein
    einmalig registrierter, dokumentweiter Klick-Handler (analog zu #16)
    schaltet zwischen beiden per ``.editing``-Klasse um. Kein Roundtrip zum
    Server ist noetig, um in den Edit-Modus zu wechseln; nur das Speichern
    (``update_url``) geht per HTMX.

    Fields:
        value: str — aktueller Wert (Anzeige- und Editor-Default)
        update_url: str — HTMX-POST-Ziel beim Speichern
        name: str — Feldname im gesendeten Formular, default "value"
        input_type: "text" | "textarea" | "select" — Editor-Steuerelement
        options: list[tuple[str, str]] — (label, value)-Paare fuer "select"
        editor_id: str — HTML-id des Wrappers, default = name
        placeholder: str — Platzhalter fuer die Anzeige, wenn value leer ist
    """

    value: str = ""
    update_url: str
    name: str = "value"
    input_type: Literal["text", "textarea", "select"] = "text"
    options: list[tuple[str, str]] = []
    editor_id: str = ""
    placeholder: str = "—"

    def render(self) -> Element:
        """Erstellt Anzeige- und Editor-Zustand im selben Wrapper-Element."""
        eid = self.editor_id or self.name

        display = span(
            self.value or self.placeholder,
            cls="inline-editor-display",
            tabindex="0",
            role="button",
            aria_label=f"Edit {self.name}",
        )

        edit_form = form(
            self._render_control(),
            button("Save", type="submit", cls="inline-editor-save"),
            button("Cancel", type="button", cls="inline-editor-cancel"),
            hx_post=self.update_url,
            hx_target=f"#{eid}",
            hx_swap=HxSwap.OUTER_HTML,
            cls="inline-editor-form",
        )

        return div(
            display,
            edit_form,
            _INLINE_EDITOR_SCRIPT,
            id=eid,
            cls=merge_cls("inline-editor", self.extra_cls),
        )

    def _render_control(self) -> Element:
        """Erstellt das Eingabe-Element fuer den Editor-Zustand."""
        if self.input_type == "textarea":
            return textarea(
                self.value or None, name=self.name, cls="inline-editor-input"
            )
        if self.input_type == "select":
            return select(
                *(
                    option(lbl, value=val, selected=True if val == self.value else None)
                    for lbl, val in self.options
                ),
                name=self.name,
                cls="inline-editor-input",
            )
        return input(
            type="text",
            name=self.name,
            value=self.value or None,
            cls="inline-editor-input",
        )


_INLINE_EDITOR_SCRIPT = raw(
    "<script>"
    "if(!window.__htmforgeInlineEditorDelegated){"
    "window.__htmforgeInlineEditorDelegated=true;"
    "document.addEventListener('click',function(e){"
    "var display=e.target.closest('.inline-editor-display');"
    "var cancel=e.target.closest('.inline-editor-cancel');"
    "if(display){"
    "var wrapper=display.closest('.inline-editor');"
    "if(wrapper){"
    "wrapper.classList.add('editing');"
    "var field=wrapper.querySelector('.inline-editor-input');"
    "if(field)field.focus();"
    "}"
    "}else if(cancel){"
    "e.preventDefault();"
    "var editWrapper=cancel.closest('.inline-editor');"
    "if(editWrapper)editWrapper.classList.remove('editing');"
    "}"
    "});"
    "document.addEventListener('keydown',function(e){"
    "if(e.key!=='Escape')return;"
    "var editingWrapper=e.target.closest('.inline-editor.editing');"
    "if(editingWrapper)editingWrapper.classList.remove('editing');"
    "});"
    "}"
    "</script>"
)
