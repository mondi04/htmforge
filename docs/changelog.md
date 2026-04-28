# Changelog

All notable changes to htmforge are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning: [Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-04-29

### Fixed
- Correct LICENSE badge link to absolute GitHub URL
- Correct Docs badge link to GitHub repository

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
