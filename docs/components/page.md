# Page

`Page` is an abstract base for full HTML documents. Subclasses implement `_body_content()`.

Props include `title`, `description`, `css_urls`, `js_urls`, `inline_css`, `charset`.

Use `to_html()` to produce a string starting with `<!DOCTYPE html>`.
