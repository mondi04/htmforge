"""Release validation and build script for htmforge.

Usage:
    python release.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from pathlib import Path


def fail(message: str) -> None:
    """Print an error and exit with code 1."""
    print(f"ERROR: {message}")
    raise SystemExit(1)


def read_version() -> str:
    """Read current project version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        fail("pyproject.toml not found")

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    try:
        version = data["project"]["version"]
    except KeyError as exc:
        fail(f"Missing [project].version in pyproject.toml: {exc}")

    if not isinstance(version, str) or not version:
        fail("Invalid [project].version in pyproject.toml")
    return version


def ensure_docs_changelog_entry(path: Path, version: str) -> None:
    """Ensure docs changelog file contains an entry for the version."""
    if not path.exists():
        fail(f"Missing file: {path}")

    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"\b(?:v)?{re.escape(version)}\b")
    if not pattern.search(text):
        fail(f"No entry for version {version} found in {path}")


def ensure_overview_changelog_entry(path: Path, version: str) -> None:
    """Ensure OVERVIEW.md Change-Log section contains an entry for version."""
    if not path.exists():
        fail(f"Missing file: {path}")

    text = path.read_text(encoding="utf-8")
    section_match = re.search(
        r"^##\s+Change-Log\s*$([\s\S]*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE,
    )
    if not section_match:
        fail("OVERVIEW.md does not contain a Change-Log section")

    section = section_match.group(1)
    pattern = re.compile(rf"\b(?:v)?{re.escape(version)}\b")
    if not pattern.search(section):
        fail(f"No entry for version {version} found in OVERVIEW.md Change-Log")


def run_step(step_name: str, command: list[str]) -> None:
    """Run a command and fail with step context on error."""
    print(f"\n[{step_name}] {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        fail(f"Step failed: {step_name}")


def find_artifacts(version: str) -> tuple[Path, Path]:
    """Locate expected wheel and source tarball for version."""
    dist = Path("dist")
    wheel = dist / f"htmforge-{version}-py3-none-any.whl"
    tarball = dist / f"htmforge-{version}.tar.gz"

    if not wheel.exists() or not tarball.exists():
        fail(
            "Missing build artifacts for current version. "
            f"Expected {wheel} and {tarball}"
        )
    return wheel, tarball


def main() -> None:
    """Run release checks and build artifacts without uploading."""
    version = read_version()

    # 2. Verify OVERVIEW changelog entry
    ensure_overview_changelog_entry(Path("OVERVIEW.md"), version)

    # 3. Verify docs changelog entry
    ensure_docs_changelog_entry(Path("docs/changelog.md"), version)

    # 4. Validation suite
    run_step("pytest", [sys.executable, "-m", "pytest"])
    run_step("mypy", [sys.executable, "-m", "mypy", "htmforge/"])
    run_step("ruff check", [sys.executable, "-m", "ruff", "check", "htmforge/"])
    run_step(
        "ruff format --check",
        [sys.executable, "-m", "ruff", "format", "--check", "htmforge/"],
    )
    run_step(
        "mkdocs build --strict",
        [sys.executable, "-m", "mkdocs", "build", "--strict"],
    )

    # 5. Build distribution and verify artifacts
    run_step("python -m build", [sys.executable, "-m", "build"])
    wheel, tarball = find_artifacts(version)

    # 6. Summary
    print("\nRelease summary")
    print(f"Version:   {version}")
    print(f"Wheel:     {wheel.as_posix()}")
    print(f"Tarball:   {tarball.as_posix()}")
    print("Status:    READY FOR UPLOAD — run push.py to publish")


if __name__ == "__main__":
    main()