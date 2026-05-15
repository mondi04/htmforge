# Release Notes — v0.4.0

## What's new

### `Component.to_json()`
All components now expose a `to_json()` method that returns a dict with two keys:

```python
component.to_json()
# {"html": "
...", "component": "Div"}
```

Useful for API endpoints that need to return rendered HTML alongside metadata.

### Migration to hatch-vcs
The project now uses `hatch-vcs` for version management. The version is derived
automatically from the Git tag — no manual `__version__` string required.

### Trusted Publishing
PyPI releases are now fully automated via OpenID Connect (Trusted Publishing).
See [docs/guide/trusted-publishing.md](guide/trusted-publishing.md) for setup details.

## Upgrade

```bash
pip install --upgrade htmforge
```

No breaking changes. All v0.3.x components are fully compatible.
