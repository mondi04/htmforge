# Page

`Page` is an abstract base for full HTML documents. Subclasses implement `_body_content()`.

```python
from htmforge.components.page import Page
from htmforge.core.element import Element


class DemoPage(Page):
    def _body_content(self) -> list[Element | str | None]:
        return []


print(DemoPage(title="Demo").to_html())
```

## Props

| Name | Type | Default | Notes |
|------|------|---------|-------|
| `title` | `str` | required | document title |
| `description` | `str` | `""` | optional meta description |
| `css_urls` | `list[str]` | `[]` | stylesheet URLs added to `<head>` |
| `js_urls` | `list[str]` | `[]` | script URLs added before `</body>` |
| `inline_css` | `str` | `""` | inline CSS wrapped in `<style>` |
| `charset` | `str` | `utf-8` | charset meta value |
| `lang` | `str` | `"en"` | Sets the `lang` attribute on the `<html>` element |

## Rendered HTML

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Demo</title>
  </head>
  <body>
    <!-- body content omitted -->
```
