"""Tests fuer die Behavioral-Affordance-Komponenten (#26)."""

from __future__ import annotations

from htmforge.components import AutocompleteInput, InfiniteScrollList, InlineEditor
from htmforge.htmx import HxTrigger


class TestAutocompleteInput:
    """Tests fuer ``AutocompleteInput``."""

    def test_renders_input_and_listbox(self) -> None:
        """Input und leere Listbox werden gerendert."""
        html = AutocompleteInput(name="q", search_url="/search").to_html()
        assert '<input type="text" name="q"' in html
        assert 'role="listbox"' in html
        assert 'id="q-listbox"' in html

    def test_trigger_includes_min_chars_and_debounce(self) -> None:
        """hx-trigger enthaelt min_chars-Filter und Debounce-Delay."""
        html = AutocompleteInput(
            name="q", search_url="/search", min_chars=3, debounce_ms=250
        ).to_html()
        assert "target.value.length&gt;=3" in html
        assert "delay:250ms" in html

    def test_aria_combobox_attributes_present(self) -> None:
        """ARIA-Combobox-Attribute verlinken Input und Listbox."""
        html = AutocompleteInput(name="q", search_url="/search").to_html()
        assert 'role="combobox"' in html
        assert 'aria-controls="q-listbox"' in html
        assert 'aria-autocomplete="list"' in html

    def test_hx_get_targets_listbox(self) -> None:
        """hx-get und hx-target zeigen auf search_url/Listbox."""
        html = AutocompleteInput(name="q", search_url="/search").to_html()
        assert 'hx-get="/search"' in html
        assert 'hx-target="#q-listbox"' in html


class TestInfiniteScrollList:
    """Tests fuer ``InfiniteScrollList``."""

    def test_renders_initial_items(self) -> None:
        """Initial uebergebene Items werden als li gerendert."""
        html = InfiniteScrollList(items=["Item 1", "Item 2"]).to_html()
        assert html.count('class="infinite-scroll-item"') == 2
        assert "Item 1" in html
        assert "Item 2" in html

    def test_sentinel_rendered_when_next_page_url_set(self) -> None:
        """Sentinel-Element mit hx-Attributen wird bei next_page_url gerendert."""
        html = InfiniteScrollList(
            items=["A"], next_page_url="/items?page=2", list_id="items"
        ).to_html()
        assert 'id="items-sentinel"' in html
        assert 'hx-get="/items?page=2"' in html
        assert 'hx-trigger="revealed"' in html
        assert 'hx-target="#items-sentinel"' in html

    def test_no_sentinel_without_next_page_url(self) -> None:
        """Ohne next_page_url wird kein Sentinel gerendert (letzte Seite)."""
        html = InfiniteScrollList(items=["A"]).to_html()
        assert "infinite-scroll-sentinel" not in html

    def test_custom_trigger(self) -> None:
        """Ein alternativer Trigger (z.B. intersect) wird uebernommen."""
        html = InfiniteScrollList(
            items=[], next_page_url="/next", trigger=HxTrigger.INTERSECT
        ).to_html()
        assert 'hx-trigger="intersect"' in html


class TestInlineEditor:
    """Tests fuer ``InlineEditor``."""

    def test_renders_display_and_form(self) -> None:
        """Anzeige-Span und Editor-Formular werden beide gerendert."""
        html = InlineEditor(value="Ada", update_url="/save").to_html()
        assert 'class="inline-editor-display"' in html
        assert "<form" in html
        assert 'hx-post="/save"' in html

    def test_empty_value_shows_placeholder(self) -> None:
        """Leerer value zeigt den Platzhalter in der Anzeige."""
        html = InlineEditor(update_url="/save").to_html()
        assert "—" in html

    def test_text_input_type_renders_input(self) -> None:
        """Default input_type='text' rendert ein input-Element."""
        html = InlineEditor(value="Ada", update_url="/save").to_html()
        assert 'class="inline-editor-input"' in html
        assert '<input type="text" name="value" value="Ada"' in html

    def test_textarea_input_type(self) -> None:
        """input_type='textarea' rendert ein textarea-Element."""
        html = InlineEditor(
            value="Bio text", update_url="/save", input_type="textarea"
        ).to_html()
        assert "<textarea" in html
        assert "Bio text</textarea>" in html

    def test_select_input_type_marks_selected_option(self) -> None:
        """input_type='select' markiert den passenden Wert als selected."""
        html = InlineEditor(
            value="admin",
            update_url="/save",
            input_type="select",
            options=[("Admin", "admin"), ("User", "user")],
        ).to_html()
        assert '<option value="admin" selected>Admin</option>' in html

    def test_hx_target_uses_editor_id(self) -> None:
        """hx-target verweist auf die id des Wrapper-Elements."""
        html = InlineEditor(
            value="Ada", update_url="/save", editor_id="bio-editor"
        ).to_html()
        assert 'id="bio-editor"' in html
        assert 'hx-target="#bio-editor"' in html
