# Contributing to htmlkit

Thank you for your interest in contributing!

## Setup

```bash
git clone https://github.com/DEIN-USERNAME/htmlkit.git
cd htmlkit
pip install -e ".[dev]"
```

Run tests and type checks:

```bash
pytest               # run all tests
mypy htmlkit/        # strict type check
ruff check htmlkit/  # lint
ruff format htmlkit/ # format
```

## Workflow

1. Fork the repository and create a branch: `git checkout -b feat/my-feature`
2. Write your code and add tests — all new public functions need a docstring
3. Make sure `pytest`, `mypy htmlkit/`, and `ruff check htmlkit/` all pass
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

### 1. New HTML elements (`details`, `summary`, `dialog`)

Add factory functions to `htmlkit/elements/__init__.py` following the existing
pattern. Each function needs a one-line docstring and an entry in `__all__`.
An HTML5 reference: https://developer.mozilla.org/en-US/docs/Web/HTML/Element

### 2. New ready-made component (Breadcrumb, Badge, or Spinner)

Create `htmlkit/components/breadcrumb.py` (or badge/spinner) as a subclass of
`Component`, export it from `htmlkit/components/__init__.py`, and add tests in
`tests/test_components.py`. Follow the structure of the existing `Alert`
component.

### 3. Framework integration tests (Flask, Django)

Add an optional test file `tests/test_framework_adapters.py` that checks
`component.to_flask()` and `component.to_django()` return the correct response
types. The tests should be skipped automatically when flask/django are not
installed (use `pytest.importorskip`).
