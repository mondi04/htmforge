# Contributing to htmforge

Thank you for your interest in contributing!

## Setup

```bash
git clone https://github.com/mondi04/htmforge.git
cd htmforge
pip install -e ".[dev]"
```

Run tests and type checks:

```bash
pytest               # run all tests
mypy htmforge/        # strict type check
ruff check htmforge/  # lint
ruff format htmforge/ # format
```

## Workflow

1. Fork the repository and create a branch: `git checkout -b feat/my-feature`
2. Write your code and add tests — all new public functions need a docstring
3. Make sure `pytest`, `mypy htmforge/`, and `ruff check htmforge/` all pass
4. Open a pull request against `main` with a clear description

## Coding Standards

- **Formatting:** `ruff format` with the project config (88 chars, double quotes)
- **Linting:** `ruff check` must pass with zero warnings
- **Types:** `mypy --strict` must pass; annotate every function signature
- **Docstrings:** All public classes and functions require a Google-style docstring
- **Tests:** Every new feature needs at least one positive and one edge-case test

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix   | When to use                          |
|----------|--------------------------------------|
| `feat:`  | New feature or component             |
| `fix:`   | Bug fix                              |
| `docs:`  | Documentation only                   |
| `test:`  | Adding or fixing tests               |
| `chore:` | Build, CI, dependency updates        |
| `refactor:` | Code change without behavior change |

Examples:
```
feat: add Breadcrumb component
fix: escape attribute values in _render_attrs
docs: add FormField usage example to README
```

## Good First Issues

If you're new to the project, these are great places to start:

### 1. Framework integration tests

Create `tests/test_framework_adapters.py` and add tests that check
`to_flask()` and `to_django()` return the correct response types. Use
`pytest.importorskip` so the tests skip when Flask or Django are not
installed.

### 2. DataTable typed rows

Add an optional `dict_rows: list[dict[str, str]]` field to
`htmforge/components/table.py`. When it is provided, render rows in header
order using the header keys.

### 3. Spinner component

Create `htmforge/components/spinner.py` as a loading indicator component with
size variants (`sm`/`md`/`lg`) rendered as a `div` with CSS class
`spinner spinner-{size}`. Export it from `components/__init__.py` and add
tests in `tests/test_components.py`.
