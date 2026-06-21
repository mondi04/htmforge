# Contributing to htmforge

Thank you for your interest in contributing!

## Before you open a PR
 
- **PRs target `develop`, not `main`.** `main` only receives merges from
  `develop` via release PRs (see "Release Process" below) — opening a PR
  directly against `main` will need to be redirected before it can be
  reviewed.
- Open an issue first for anything beyond a trivial fix.
  New components or API changes need prior discussion.
- Check that a similar issue or PR doesn't already exist.

## Setup

```bash
git clone https://github.com/mondi04/htmforge.git
cd htmforge
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
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
4. Open a pull request **against `develop`** with a clear description

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

## Release Process (Maintainers)

> This section is only relevant for repository maintainers merging PRs into
> `main`. Contributors can ignore it.

Releases are triggered automatically by a tag push, which is itself created
automatically when a PR is merged into `main` — **if** the merge commit title
follows a specific convention.

### How it works

1. A PR targeting `develop` is reviewed and merged as usual — nothing special here.
2. When `develop` is ready for a release, open a PR from `develop` into `main`.
3. When merging that PR via the GitHub UI, GitHub pre-fills the merge commit
   title with `Merge pull request #X from mondi04/develop`. **Overwrite this
   title** with: ```release: vX.Y.Z``` (e.g. `release: v0.4.3`), matching the next version per
   [Semantic Versioning](https://semver.org/). This must be typed manually —
   there is no default that produces a release.
4. On merge, the **Auto Tag** workflow (`.github/workflows/auto-tag.yml`) runs
   on `main` and:
   - Reads the merge commit title.
   - If it matches `release: vX.Y.Z` **at the start of the message**, creates
     and pushes tag `vX.Y.Z`, then fast-forwards `develop` onto `main`.
   - If it does **not** match, the workflow **fails** (red ❌ in the Actions
     tab) — no tag is created. This is intentional: it makes a forgotten
     title change immediately visible instead of silently doing nothing.
5. The tag push triggers the existing **Release** workflow
   (`.github/workflows/release.yml`), which runs tests, builds the package,
   publishes to PyPI, creates the GitHub Release (using the matching section
   from `docs/changelog.md`), and deploys docs.

### Normal merges into `main` without a release

Not every merge into `main` needs to ship a release. If you merge without
changing the commit title to `release: vX.Y.Z`, the Auto Tag workflow will
fail with a red ❌. **This failure is expected and harmless** for non-release
merges — it does not block or revert the merge itself, it only means no tag
was created. It exists purely as a visible reminder; it's safe to ignore for
merges that were never meant to be a release.

### Before merging a release PR

- [ ] `docs/changelog.md` has a `## [X.Y.Z] - YYYY-MM-DD` section for the new
      version (the Release workflow extracts its body for the GitHub Release
      notes — falls back to a generic message if missing).
- [ ] You're merging `develop` → `main` (not some other branch).

Note: the package version itself does **not** need to be set anywhere by
hand — `pyproject.toml` uses `hatch-vcs` (`dynamic = ["version"]`,
`tool.hatch.version.source = "vcs"`), so the version is derived directly from
the git tag at build time.

### Things that can go wrong

| Symptom | Cause | Fix |
|---|---|---|
| Auto Tag fails with "kein Tag-Pattern gefunden" | Forgot to overwrite the merge commit title | If this should've been a release: revert/re-merge with the correct title. Otherwise: ignore, expected for non-release merges. |
| Auto Tag fails with "Tag existiert bereits" | Version number wasn't bumped, or this version was already released | Bump the version and re-merge with a new tag. |
| `develop` not synced after a release | `develop` had commits not yet in `main` (fast-forward not possible), or push to `develop` was rejected by branch protection | Sync manually: `git checkout develop && git merge --ff-only main && git push`. |
| Pre-release tags (`v1.2.3-beta`) | Not currently supported — the version regex only matches plain `X.Y.Z`, the suffix would be silently dropped from the tag | Avoid pre-release tags via this workflow for now; tag manually if ever needed. |

## Good First Issues

If you're new to the project, these are great places to start:

### 1. Admin Panel Example: Screenshot

Add at least one screenshot to `examples/admin-panel/README.md`. Run the admin
panel locally, take a screenshot of the users page, save it as
`examples/admin-panel/static/screenshot.png`, and reference it in the README.

### 2. DataTable: render Component cells in legacy rows mode

Currently `rows: list[list[str]]` only supports strings. Add support for
`list[list[str | Element]]` so Element values in legacy rows are rendered
correctly, not just stringified.

### 3. Page: add lang attribute support

Add an optional `lang: str = "en"` field to `Page` that sets
`<html lang="en">`. Update the `render()` method to pass it to the `html()`
element. Add a test in `tests/test_components.py`.
