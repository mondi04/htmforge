# Spinner

Accessible loading indicator with configurable size and label for ARIA compatibility.

```python
from htmforge.components import Spinner, SpinnerSize

Spinner(size=SpinnerSize.LG, label="Loading data...").to_html()
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `size` | `SpinnerSize` | `SpinnerSize.MD` | Size variant: SM, MD, or LG |
| `label` | `str` | `"Loading"` | ARIA label for accessibility |

## Rendered HTML

```html
<div class="spinner spinner-lg" role="status" aria-label="Loading data..."></div>
```

SpinnerSize options: `SM` (small), `MD` (medium), `LG` (large).
