"""In-memory data store for the admin panel demo."""

from __future__ import annotations

from datetime import date, timedelta
from typing_extensions import Literal, TypedDict

UserRole = Literal["admin", "editor", "viewer"]


class User(TypedDict):
    """Typed user record stored in memory."""

    id: int
    name: str
    email: str
    role: UserRole
    created_at: str


_SEED_USERS: tuple[tuple[str, str, UserRole], ...] = (
    ("Ada Lovelace", "ada@example.com", "admin"),
    ("Grace Hopper", "grace@example.com", "editor"),
    ("Margaret Hamilton", "margaret@example.com", "viewer"),
    ("Alan Turing", "alan@example.com", "viewer"),
    ("Katherine Johnson", "katherine@example.com", "editor"),
    ("Dennis Ritchie", "dennis@example.com", "viewer"),
    ("Barbara Liskov", "barbara@example.com", "admin"),
    ("Edsger Dijkstra", "edsger@example.com", "editor"),
    ("Donald Knuth", "donald@example.com", "viewer"),
    ("Frances Allen", "frances@example.com", "admin"),
    ("Linus Torvalds", "linus@example.com", "viewer"),
    ("Radia Perlman", "radia@example.com", "editor"),
    ("Bjarne Stroustrup", "bjarne@example.com", "viewer"),
    ("Tim Berners-Lee", "tim@example.com", "admin"),
    ("Guido van Rossum", "guido@example.com", "editor"),
    ("Hedy Lamarr", "hedy@example.com", "viewer"),
    ("James Gosling", "james@example.com", "admin"),
    ("Jennifer Doudna", "jennifer@example.com", "editor"),
    ("Margaret Oakley", "margaret.o@example.com", "viewer"),
    ("Joy Buolamwini", "joy@example.com", "admin"),
    ("Matz Matsumoto", "matz@example.com", "viewer"),
    ("Sandi Metz", "sandi@example.com", "editor"),
    ("Ken Thompson", "ken@example.com", "viewer"),
)

_USERS: list[User] = []


def _seed_users() -> list[User]:
    start = date(2026, 1, 1)
    records: list[User] = []
    for index, (name, email, role) in enumerate(_SEED_USERS, start=1):
        records.append(
            User(
                id=index,
                name=name,
                email=email,
                role=role,
                created_at=(start + timedelta(days=index - 1)).isoformat(),
            )
        )
    return records


_USERS = _seed_users()


def _sorted_users() -> list[User]:
    return sorted(_USERS, key=lambda user: user["id"], reverse=True)


def _matches_query(user: User, query: str) -> bool:
    if not query:
        return True
    needle = query.casefold()
    return any(needle in str(user[field]).casefold() for field in ("name", "email", "role"))


def list_users(q: str = "", page: int = 1, per_page: int = 5) -> tuple[list[User], int]:
    """Return the current page slice and the total number of matches."""

    filtered = [user.copy() for user in _sorted_users() if _matches_query(user, q.strip())]
    total = len(filtered)
    if total == 0:
        return [], 0

    total_pages = max(1, (total + per_page - 1) // per_page)
    current_page = max(1, min(page, total_pages))
    start = (current_page - 1) * per_page
    return filtered[start : start + per_page], total


def get_user(user_id: int) -> User | None:
    """Fetch a single user by id."""

    for user in _USERS:
        if user["id"] == user_id:
            return user.copy()
    return None


def create_user(*, name: str, email: str, role: UserRole) -> User:
    """Create a new user record."""

    next_id = max((user["id"] for user in _USERS), default=0) + 1
    user: User = {
        "id": next_id,
        "name": name.strip(),
        "email": email.strip(),
        "role": role,
        "created_at": date.today().isoformat(),
    }
    _USERS.append(user)
    return user.copy()


def update_user(user_id: int, *, name: str, email: str, role: UserRole) -> User:
    """Update an existing user record."""

    for index, user in enumerate(_USERS):
        if user["id"] == user_id:
            _USERS[index] = {
                **user,
                "name": name.strip(),
                "email": email.strip(),
                "role": role,
            }
            return _USERS[index].copy()
    raise KeyError(f"User {user_id} not found")


def delete_user(user_id: int) -> bool:
    """Delete a user record."""

    for index, user in enumerate(_USERS):
        if user["id"] == user_id:
            del _USERS[index]
            return True
    return False


def reset_users() -> None:
    """Reset all users to the seed data."""

    global _USERS
    _USERS = _seed_users()