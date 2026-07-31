# Changelog

All notable changes to htmforge are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/).

## [0.6.0] - 2026-07-31

### Added
- `DashboardLayout` + `Widget`: grid-based widget dashboards (#24)
- `AutocompleteInput`, `InfiniteScrollList`, `InlineEditor`: behavioral affordance components covering debounced search, infinite scroll, and click-to-edit patterns (#26)
- `htmforge.auth`: `LoginForm`, `LogoutButton` components and `requires_auth`/`role_required` render guards (#25)
- `Component.css_files` / `Component.js_files` + `htmforge.core.assets.collect_assets()`: component-level asset declaration, auto-injected (deduplicated) by `Page` (#3)
- `Component.fast_construct()`: opt-in validation-skip constructor for hot loops over components with expensive nested validation (#1)
- `htmforge.devtools`: polling-based dev-mode auto-reload (`DevReloadWatcher`, `dev_reload_script()`) (#5)
- `htmforge.contrib.tailwind`: optional Tailwind-styled starter components — `Button`, `Card`, `Alert`, `Badge` (#6)
- `aria-describedby` linking error messages to their inputs across `FormField`, `SelectField`, `CheckboxField`, `RadioGroup` (#17)
- CSRF hidden-field pattern documented on `Form` (#17)

### Changed
- `Element.to_html()` now writes into a shared buffer (`_write()`) instead of recursively joining per-level strings, avoiding repeated string copies on deeply nested trees (#18)
- Default strings switched from German to English: `Alert.close_label` / `Modal.close_label` ("Close"), `Form.submit_label` ("Submit"), `DataTable.empty_message` ("No entries") (#17)
- `Modal`'s inline script is now a single, idempotent, document-level delegated click listener instead of one per instance, preventing duplicate listeners and `InvalidStateError` with multiple modals on one page (#16)

### Fixed
- `FormField` no longer renders a `<label>`/error `<div>` for `InputType.HIDDEN` (#14)
- `DataTable` sort links use `&` instead of a second `?` when `sort_url` already has a query string (#15)
- `Component.to_json()` docstring example now matches actual output (#19)

## [0.5.1] - 2026-06-21

### Fixed
- `Component.clone()`: fixed a `TypeError` ("Can't instantiate abstract class
  Component...") raised whenever a component held a field typed as
  `Component` or `list[Component]` — e.g. `Form.fields`, `FormGroup.fields`,
  or `Component` cell values inside `DataTable.dict_rows`. `clone()`
  previously round-tripped through `model_dump()`, which serialized nested
  components using their declared abstract `Component` type instead of
  their actual runtime subclass, producing an empty dict and a failed
  reconstruction. `clone()` now reads field values directly and deep-copies
  them before applying overrides, preserving the concrete runtime type of
  nested components. (#13, #21)

## [0.5.0] - 2026-06-20

### Added
- `Form.from_model(model, action="", **kwargs)`: generates a `Form` directly from a Pydantic v2 model
- `htmforge.components.form_model.fields_from_model(model)`: introspection helper, maps model fields to `FormField`/`CheckboxField`/`SelectField`
- `InputType.TEXTAREA`: new `FormField` input type, renders `<textarea>`
- `FormField.min` / `FormField.max`: numeric bounds rendered on `<input type="number">`

### Changed
- `Form.action` is now optional (default `""`) instead of required

### Fixed
- Default theme (`docs/assets/css/htmforge-theme.css` + `examples/admin-panel/static/admin.css`): `CheckboxField`/`RadioGroup` inputs no longer inherit full-width text-input styling (`width: 100%`, large padding, `border-radius: 14px`), which previously rendered checkboxes/radios as oversized pill shapes
- `.checkbox-field` / `.radio-item`: switched from `display: grid` to `display: flex` so the input sits inline with its label instead of stacking on its own row
- `.checkbox-field label` now included in the bold-label rule (was previously unstyled, inconsistent with other field labels)
- `<textarea>` (new via `InputType.TEXTAREA`) now has matching border, padding, and focus styling instead of falling back to unstyled browser defaults; added `min-height`, vertical `resize`, and `line-height` for usability
- Generic input focus-state block extended to cover `number`, `tel`, `url`, and `textarea` (previously only `text`/`email`/`search`/`password`/`select` were covered)

## [0.4.3] - 2026-06-20

### Added
- `.github/workflows/auto-tag.yml`: automatically tags `main` on merge when the merge commit title starts with `release: vX.Y.Z`, then fast-forwards `develop` onto `main`. Fails visibly (red ❌) if no valid release pattern is found, so a forgotten title change is never silent.
- Documented the full release process in `CONTRIBUTING.md` (Maintainers section), including the manual merge-title step and a troubleshooting table.

## [0.4.2] - 2026-06-20

### Added
- `Component.extra_cls`: optional CSS class field on the base `Component`, merged additively with each component's default class via `merge_cls()` (does not replace it)
- `htmforge.core.element.merge_cls()`: joins multiple class strings, skipping empty/`None` parts, returns `None` if all parts are empty (avoids emitting `class=""`)
- `extra_cls` wired up in Alert, Badge, Breadcrumb, Dropdown, FormField, Modal, Pagination, SearchInput, Spinner, Table, Tabs, Toast, Accordion, SelectField, CheckboxField, RadioGroup, FormGroup, Form
- Styling guide (docs/guide/styling.md): CSS class reference for all components
- Optional default theme stylesheet (docs/assets/css/htmforge-theme.css)
- Tabs, Accordion, Dropdown CSS added to example admin theme

### Changed
- `RadioGroup`: root `<fieldset>` now always renders `class="radiogroup"` (previously unstyled)
- `Form`: root `<form>` now always renders `class="form"` (previously unstyled)
- `FormGroup.group_cls` kept for backwards compatibility; merges additively with the new `extra_cls`

### Fixed
- Components silently accepted and discarded an unsupported `cls` kwarg due to Pydantic's default `extra="ignore"` behavior; there was previously no supported way to add a custom CSS class to a pre-built component

## [0.4.1] - 2026-06-16

### Added
- GitHub issue templates: bug.yml (bug reports), feature.yml (feature requests), config.yml (template config)
- PR template with checklist for tests, type checking, linting, docstrings, conventional commits
- Updated CONTRIBUTING.md with full setup guide, workflow, and coding standards

### Changed
- Release workflow: moved from local release.py/push.py scripts to GitHub Actions
- release.yml now uses Trusted Publishing (OIDC) instead of PyPI API tokens

### Removed
- release.py: version detection and validation now in GitHub Actions workflow
- push.py: PyPI uploads now handled by gh-action-pypi-publish

### Fixed
- (none for this patch)

## [0.4.0] - 2026-05-15

### Added
- Page: lang field (default "en") sets lang attribute on <html> element for accessibility
- Component: to_json() method returns {"html": ..., "component": ...} for API endpoints
- CI: optional Trusted Publishing workflow (publish.yml) — manual trigger, replaces local token

### Changed
- Build: migrated to hatch-vcs for single-source-of-truth versioning via git tags
- release.py and push.py: read version from git tag instead of pyproject.toml

## [0.3.3] - 2026-05-15

### Fixed
- README: all relative links replaced with absolute GitHub URLs for PyPI compatibility
- DataTable component reference updated to document ColumnDef, dict_rows, sort_url,
  current_sort, sort_dir, and empty_message parameters
- docs/guide/components.md: fixed broken code block fences and garbled method names

### Changed
- CONTRIBUTING.md: Good First Issues updated to reflect actual open tasks
- OVERVIEW.md: test count and roadmap updated

## [0.3.2] - 2026-05-15

### Fixed
- DataTable: Component and Element cell values in dict_rows now render correctly — Component cells call `.render()`, Element cells are passed directly to `td()`
- Admin panel example: BaseAdminPage no longer calls undeclared `_content()` hook; all subclasses implement `_body_content()` directly

### Changed
- Release workflow: added `validate` job that ensures tag points to main before building
- pyproject.toml: extended keywords with `dominate`, `htpy`, `html-builder`, `template-free`

## [0.3.1] - 2026-05-06

### Documentation
- Completed all missing component reference pages:
  Spinner, Tabs, Toast, Accordion, Dropdown, SelectField,
  CheckboxField, RadioGroup, FormGroup, Form
- Fixed MkDocs navigation to include full component list
- Corrected broken relative links in release notes
- Fixed Quickstart code blocks (proper fenced syntax)
- Expanded homepage feature list with full capabilities overview

### Changed
- README.md fully revised for improved clarity, structure, and onboarding experience

### Quality
- mkdocs build passes with --strict (0 warnings, 0 errors)

## [0.3.0] - 2026-05-06

### Block F — DataTable Enhancements
- `ColumnDef` class: Structured column definition (key, label, sortable, width)
- `dict_rows` support: Render from list[dict[str, str]] (backward-compatible with list[list[str]])
- Sortable headers: ColumnDef.sortable renders hx-get links with sort/direction parameters
- Sort tracking: sort_url, current_sort, sort_dir fields for sort direction flip logic
- Full API stability: No breaking changes to existing DataTable usage

### Block G — New Components (5)
- `Spinner`: Accessible loading indicator with SpinnerSize enum (SM/MD/LG), role/aria-label
- `Tabs`: Tab navigation with HTMX lazy-load per inactive tab, active state tracking
- `Toast`: Timed notifications with ToastVariant enum, hx-swap-oob, auto-dismiss duration
- `Accordion`: Collapsible sections using `<details>`/`<summary>`, open_index control
- `Dropdown`: Trigger button with dropdown menu items, optional HTMX toggle URL
- **25 component tests** covering render logic, HTMX attributes, edge cases

### Block H — Forms System (5 Components)
- `SelectField`: Dropdown select with typed options list, optional label
- `CheckboxField`: Single checkbox with inline label and error display
- `RadioGroup`: Fieldset with multiple radio inputs, legend, error support
- `FormGroup`: Layout container for multiple fields with optional legend
- `Form`: Main form wrapper with auto-error injection pattern and HTMX submit
  - Auto-error injection: Matches field names to errors dict, clones field with error boundary
  - HTMX integration: Optional hx_post, hx_target, hx_swap for progressive enhancement
- **22 form tests** covering form structure, error injection, HTMX attributes

### Block I — API Extensions
- `Element.__eq__` and `__hash__`: Compare rendered HTML for equality, enable deduplication
- `Component.clone(**overrides)`: Create new instance with changed properties
- `Component.to_fragment()`: Explicit HTMX fragment rendering method
- `htmforge.render()`: Top-level convenience function for Element/Component rendering
- `htmforge.when()`: Conditional rendering helper (returns Element or None)

### Block J — Testing Infrastructure
- **tests/test_framework_adapters.py** (14 tests):
  - FastAPI adapter: 3 tests for to_fastapi() HTMLResponse integration
  - Flask adapter: 6 tests for to_flask() Response with content-type
  - Django adapter: 5 tests (auto-skipped if not installed)
  - Error handling: ImportError tests for missing framework imports
- **tests/test_snapshots.py** (21 tests):
  - Regression detection via HTML snapshots
  - Auto-create snapshots in tests/snapshots/ on first run
  - Compare rendered HTML against stored snapshots on subsequent runs
  - Full component coverage: all 20+ components
- **tests/test_performance.py** (5 benchmarks):
  - Element rendering: 1000 iterations <1 second
  - Nested elements (ul/li): 1000 iterations <1 second
  - DataTable (10 rows): 1000 renders <2 seconds
  - Alert rendering: 1000 renders <1 second
  - render() helper: 1000 calls <1 second
- **tests/snapshots/ directory**: Machine-generated HTML snapshots (added to .gitignore)

### Quality & Testing
- **238 tests passing** + 5 skipped (Django optional dependency)
- **mypy --strict**: All 22 source files clean, 0 errors
- **ruff**: Lint and format checks passing
- **Full backwards compatibility**: All v0.2.x APIs continue working
- Type checking: mypy strict mode, 22 source files
- Linting: ruff checks pass, 22 files formatted
- Documentation: Full API reference for new components
- Component organization: Clear categorization in README (Layout, Data Display, Navigation, Forms)

## [0.2.2] - 2026-04-29

### Added
- Component reference pages now include full props tables with
	types, defaults, and descriptions for all fields
- Rendered HTML output blocks on all component pages (Alert,
	Badge, Breadcrumb, DataTable, FormField, Modal, Page,
	Pagination, SearchInput)
- Quickstart guide rewritten with complete runnable Flask example
	including rendered output
- Core Concepts page: attribute mapping table and expanded
	Mermaid architecture diagram
- Framework Adapters guide: full embedded FastAPI, Flask, and
	Django code examples
- Contributing guide: full CONTRIBUTING.md content embedded
	in docs site

### Fixed
- OVERVIEW.md merge conflict in Roadmap table resolved
- Spinner row removed from Ready-made components table
	(not yet implemented)
- Next Implementation Blocks section updated to Blocks F–J
- CONTRIBUTING.md Good First Issues updated to reflect
	actual open tasks

## [0.2.1] - 2026-04-29

### Fixed
- README LICENSE badge now links to absolute GitHub URL
	(https://github.com/mondi04/htmforge/blob/main/LICENSE)
- README Docs badge corrected to point to GitHub Pages
	(https://mondi04.github.io/htmforge/)

## [0.2.0] - 2026-04-28

### Added
- 25 new element factories: dialog, details, summary, fieldset,
	legend, progress, meter, kbd, abbr, time, address, mark, small,
	sub, sup, caption, colgroup, col, source, track, audio, video,
	picture, map_, area, iframe, canvas
- Badge component with BadgeVariant enum (default/primary/success/
	warning/danger)
- Breadcrumb component with aria-current support
- Modal component with HTMX content loading via data-attribute +
	inline script (no onclick escaping issues)
- SearchInput component with configurable debounce via search_url
	and search_target fields
- hx_keyup_delay(ms) helper function in htmforge.htmx
- Component.__repr__ for readable debug output
- mkdocs-material documentation site with full API reference,
	guides, and example apps
- GitHub Actions: docs deploy to GitHub Pages (docs.yml)
- GitHub Actions: automated GitHub Release on tag push (release.yml)
- Python 3.13 added to CI test matrix
- MIT + Commons Clause license (replaces pure MIT)
- release.py and push.py scripts for reproducible PyPI releases
- Flask example app (examples/flask_demo.py)

### Fixed
- Alert dismiss button replaced with JS onclick (was broken:
	hx-get="" triggered a GET to the current URL)
- Modal trigger button used onclick with markupsafe-escaped single
	quotes breaking JS; replaced with data-modal-target attribute
	and inline script
- Page._body_content None values now explicitly filtered before
	passing to body() element
- __version__ fallback changed from "0.1.2" to "0.0.0" to avoid
	confusion when package is not pip-installed

### Changed
- SearchInput fields renamed: hx_url → search_url,
	hx_target → search_target (avoided conflict with inherited
	Component HTMX fields)

## [0.1.2] - 2026-03-12

### Added
- DataTable component with optional HTMX reload
- Alert component with AlertVariant enum and JS-dismissible option
- Pagination component with Previous/Next and HTMX targeting
- Page abstract base class with DOCTYPE, head elements, css/js URLs
- FormField component with 8 input types and error display
- safe_html() function for trusted HTML content
- raw() helper for unescaped script/style content
- Framework adapters: to_fastapi(), to_flask(), to_django()
- FastAPI demo app (examples/fastapi_demo.py)

### Fixed
- importlib.metadata version with PackageNotFoundError fallback
- Pagination.hx_target made optional (empty string default)
- __init_subclass__ signature corrected to **kwargs: Any
- Page removed from components/__init__.py (it is abstract)
- Deprecated ANN101/ANN102 ruff ignores removed from pyproject.toml

## [0.1.0] - 2026-03-12

### Added
- Element class: recursive to_html(), void elements, attribute
	mapping (cls→class, for_→for, hx_get→hx-get), XSS escaping
	via markupsafe
- Component abstract base class: Pydantic v2, validate_assignment,
	abstract render(), to_html(), htmx_attrs()
- 60+ HTML5 element factories in htmforge.elements
- HTMX enums: HxSwap, HxTrigger, HxTarget, HxPushUrl
- py.typed marker (PEP 561)
- CI via GitHub Actions: pytest + mypy + ruff, Python 3.11/3.12
- MIT License
