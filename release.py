"""
htmforge — Release Script
Usage: python release.py
Merged develop → main, released auf PyPI, synct develop zurück.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PYTHON = sys.executable

def ok(msg):   print(f"[OK]   {msg}")
def info(msg): print(f"[...] {msg}")
def fail(msg):
    print(f"[ERR] {msg}")
    sys.exit(1)

def confirm(prompt):
    answer = input(f"\n{prompt} [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        sys.exit(0)

def run(cmd, check=True):
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        fail(f"Fehlgeschlagen: {cmd}")
    return result

def get(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

print()
print("=" * 42)
print("  htmforge Release Script")
print("=" * 42)

# ── Version erfragen ──────────────────────────────────────────────────────────
pyproject_path = Path("pyproject.toml")
pyproject = pyproject_path.read_text(encoding="utf-8")
match = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE)
if not match:
    fail("Version nicht in pyproject.toml gefunden")
last_version = match.group(1)

print(f"\n  Aktuelle Version: {last_version}")
new_version = input("  Neue Version eingeben (z.B. 0.2.0): ").strip().lstrip("v")
if not re.match(r"^\d+\.\d+\.\d+$", new_version):
    fail(f"Ungültiges Format: '{new_version}' — bitte X.Y.Z verwenden")

print(f"\n  {last_version}  →  {new_version}")
confirm(f"Release v{new_version} starten?")

# ── Sicherstellen auf develop ─────────────────────────────────────────────────
branch = get("git rev-parse --abbrev-ref HEAD")
if branch != "develop":
    info(f"Wechsle von '{branch}' zu develop...")
    run("git checkout develop")

# ── Uncommitted changes committen ─────────────────────────────────────────────
status = subprocess.run("git diff --quiet && git diff --cached --quiet", shell=True)
if status.returncode != 0:
    info("Uncommitted changes — werden automatisch committet...")
    run("git add -A")
    run(f'git commit -m "chore: pre-release cleanup for v{new_version}"')

# ── Tests ─────────────────────────────────────────────────────────────────────
print("\n--- Tests ---")
run(f"{PYTHON} -m pytest --tb=short -q")
ok("Alle Tests bestanden")

# ── Lint & Format ─────────────────────────────────────────────────────────────
print("\n--- Lint ---")
run(f"{PYTHON} -m ruff format htmforge/")
run(f"{PYTHON} -m ruff check htmforge/ --fix")
run(f"{PYTHON} -m ruff check htmforge/")
ok("ruff sauber")
run(f"{PYTHON} -m mypy htmforge/")
ok("mypy sauber")

# ── Version bumpen auf develop ────────────────────────────────────────────────
print("\n--- Version bumpen ---")
new_pyproject = re.sub(r'^version = ".*"', f'version = "{new_version}"', pyproject, flags=re.MULTILINE)
pyproject_path.write_text(new_pyproject, encoding="utf-8")
ok(f"pyproject.toml → {new_version}")

init = Path("htmforge/__init__.py")
if init.exists():
    content = init.read_text(encoding="utf-8")
    if '__version__ = "' in content:
        new_content = re.sub(r'__version__ = ".*"', f'__version__ = "{new_version}"', content)
        init.write_text(new_content, encoding="utf-8")
        ok(f"__init__.py → {new_version}")
    else:
        info("__init__.py nutzt importlib.metadata — kein Bump nötig")

# ── Build ─────────────────────────────────────────────────────────────────────
print("\n--- Build ---")
if Path("dist").exists():
    shutil.rmtree("dist")
run(f"{PYTHON} -m build")
run(f"{PYTHON} -m twine check dist/*")
ok("Build erfolgreich")

# ── Smoke test ────────────────────────────────────────────────────────────────
print("\n--- Smoke test ---")
wheels = list(Path("dist").glob("*.whl"))
if not wheels:
    fail("Kein wheel in dist/ gefunden")

venv_dir = Path(tempfile.mkdtemp())
run(f"{PYTHON} -m venv {venv_dir}")
venv_python = venv_dir / "Scripts" / "python.exe"
run(f'"{venv_python}" -m pip install "{wheels[0]}" -q')
run(f'"{venv_python}" -c "import htmforge; assert htmforge.__version__ == \'{new_version}\', f\'Version falsch: {{htmforge.__version__}}\'; print(\'OK:\', htmforge.__version__)"')
shutil.rmtree(venv_dir)
ok("Smoke test bestanden")

# ── develop committen & pushen ────────────────────────────────────────────────
print("\n--- develop → push ---")
run("git add -A")
run(f'git commit -m "chore: release v{new_version}"')
run("git push origin develop")
ok("develop gepusht")

# ── main: merge develop ───────────────────────────────────────────────────────
print("\n--- merge develop → main ---")
run("git checkout main")
run("git pull origin main")
run("git merge develop --no-ff -m \"chore: merge develop for release v" + new_version + "\"", check=False)

# Konflikt in pyproject.toml automatisch lösen (unsere Version aus develop)
conflict = subprocess.run("git diff --name-only --diff-filter=U", shell=True, capture_output=True, text=True)
if "pyproject.toml" in conflict.stdout:
    info("Konflikt in pyproject.toml — löse automatisch...")
    run("git checkout --theirs pyproject.toml")
    run("git add pyproject.toml")
    run(f'git commit -m "chore: resolve pyproject.toml conflict for v{new_version}"')

ok("develop → main gemerged")

# ── Tag & push main ───────────────────────────────────────────────────────────
print("\n--- Tag & push main ---")
run(f"git tag v{new_version}")
run("git push origin main")
run(f"git push origin v{new_version}")
ok(f"main gepusht — Tag v{new_version}")

# ── PyPI upload ───────────────────────────────────────────────────────────────
print()
confirm(f"v{new_version} jetzt auf PyPI hochladen?")
run(f"{PYTHON} -m twine upload dist/*")
ok(f"Live → https://pypi.org/project/htmforge/{new_version}/")

# ── develop synct zurück ──────────────────────────────────────────────────────
print("\n--- sync main → develop ---")
run("git checkout develop")
run("git merge main --no-ff -m \"chore: sync develop after release v" + new_version + "\"")
run("git push origin develop")
ok("develop synchronisiert")

# ── Fertig ────────────────────────────────────────────────────────────────────
print()
print("=" * 42)
print(f"  htmforge v{new_version} ist live!")
print(f"  PyPI:   https://pypi.org/project/htmforge/{new_version}/")
print(f"  GitHub: https://github.com/mondi04/htmforge/releases/new?tag=v{new_version}")
print("=" * 42)