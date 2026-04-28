from __future__ import annotations

from flask import Flask, request
from htmforge.components import DataTable, Pagination, FormField, InputType
from htmforge.components.page import Page
from htmforge.core.element import Element
from htmforge.elements import div, h1

app = Flask(__name__)

_USERS = [["Ada Lovelace", "ada@example.com"], ["Grace Hopper", "grace@example.com"]]
PAGE_SIZE = 2


class UsersPage(Page):
    users: list[list[str]]
    current_page: int = 1
    total_pages: int = 1

    def _body_content(self) -> list[Element | str | None]:
        table = DataTable(headers=["Name", "Email"], rows=self.users, hx_url="/users/table?page={page}")
        pager = Pagination(current_page=self.current_page, total_pages=self.total_pages, hx_url="/users/table?page={page}", hx_target="#users-table")

        return [div(h1("Users"), div(table, pager, id="users-table"))]


def _paginate(page: int) -> tuple[list[list[str]], int]:
    total = max(1, -(-len(_USERS) // PAGE_SIZE))
    start = (page - 1) * PAGE_SIZE
    return _USERS[start : start + PAGE_SIZE], total


@app.route("/users")
def list_users():
    page = int(request.args.get("page", 1))
    rows, total = _paginate(page)
    return UsersPage(title="Users — Flask demo", users=rows, current_page=page, total_pages=total).to_html()


@app.route("/users/table")
def users_table_fragment():
    page = int(request.args.get("page", 1))
    rows, total = _paginate(page)
    table = DataTable(headers=["Name", "Email"], rows=rows).render().to_html()
    pager = Pagination(current_page=page, total_pages=total, hx_url="/users/table?page={page}").render().to_html()
    return table + pager


if __name__ == "__main__":
    app.run(debug=True)
