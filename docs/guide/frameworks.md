# Framework Adapters

FastAPI / Flask / Django examples for returning a full page or an HTMX fragment.

- `Component.to_fastapi()` returns a `fastapi.responses.HTMLResponse` (requires `fastapi`).
- `Component.to_flask()` returns a `flask.Response` (requires `flask`).
- `Component.to_django()` returns a `django.http.HttpResponse` (requires `django`).

## FastAPI

This example returns a full page from `/users` and a fragment from `/users/table`.

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from htmforge.components import DataTable
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import div, h1


app = FastAPI()


class UsersPage(Page):
    rows: list[list[str]]

    def _body_content(self) -> list[Element | str | None]:
        return [
            div(
                h1("Users"),
                DataTable(headers=["Name", "Email"], rows=self.rows),
            )
        ]


@app.get("/users", response_class=HTMLResponse)
def users() -> str:
    return UsersPage(
        title="Users",
        rows=[["Ada Lovelace", "ada@example.com"]],
    ).to_html()


@app.get("/users/table", response_class=HTMLResponse)
def users_table() -> str:
    return DataTable(
        headers=["Name", "Email"],
        rows=[["Ada Lovelace", "ada@example.com"]],
    ).to_html()
```

## Flask

This example uses `to_flask()` on a full page route.

```python
from flask import Flask

from htmforge.components import DataTable
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import div, h1


app = Flask(__name__)


class UsersPage(Page):
    rows: list[list[str]]

    def _body_content(self) -> list[Element | str | None]:
        return [
            div(
                h1("Users"),
                DataTable(headers=["Name", "Email"], rows=self.rows),
            )
        ]


@app.route("/")
def index():
    return UsersPage(
        title="Users",
        rows=[["Ada Lovelace", "ada@example.com"]],
    ).to_flask()


if __name__ == "__main__":
    app.run(debug=True)
```

## Django

This example uses `to_django()` in a view and shows the minimal `urls.py`.

```python
# views.py
from htmforge.components import DataTable
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import div, h1


class UsersPage(Page):
    rows: list[list[str]]

    def _body_content(self) -> list[Element | str | None]:
        return [
            div(
                h1("Users"),
                DataTable(headers=["Name", "Email"], rows=self.rows),
            )
        ]


def users(request):
    return UsersPage(
        title="Users",
        rows=[["Ada Lovelace", "ada@example.com"]],
    ).to_django()
```

```python
# urls.py
from django.urls import path

from .views import users


urlpatterns = [path("users/", users)]
```
