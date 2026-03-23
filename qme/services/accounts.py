"""In-memory accounts for demo; replace with a database and real auth for production."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass

from starlette.requests import Request


@dataclass
class User:
    id: str
    email: str
    display_name: str
    main_cv: str
    life_story: str
    password_salt: bytes
    password_hash: bytes
    reqme_token: str


_users_by_id: dict[str, User] = {}
_by_email: dict[str, str] = {}
_reqme_token_to_user: dict[str, str] = {}


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)


def register_user(
    *,
    email: str,
    display_name: str,
    password: str,
    main_cv: str = "",
    life_story: str = "",
) -> tuple[str | None, User | None]:
    email_n = email.strip().lower()
    if not email_n or "@" not in email_n:
        return "Enter a valid email.", None
    if len(password) < 6:
        return "Password must be at least 6 characters.", None
    if email_n in _by_email:
        return "An account with this email already exists.", None
    uid = secrets.token_urlsafe(16)
    salt = secrets.token_bytes(16)
    pw_hash = _hash_password(password, salt)
    rtoken = secrets.token_urlsafe(12)
    user = User(
        id=uid,
        email=email_n,
        display_name=display_name.strip() or email_n.split("@")[0],
        main_cv=main_cv.strip(),
        life_story=life_story.strip(),
        password_salt=salt,
        password_hash=pw_hash,
        reqme_token=rtoken,
    )
    _users_by_id[uid] = user
    _by_email[email_n] = uid
    _reqme_token_to_user[rtoken] = uid
    return None, user


def verify_login(email: str, password: str) -> User | None:
    email_n = email.strip().lower()
    uid = _by_email.get(email_n)
    if not uid:
        return None
    user = _users_by_id.get(uid)
    if not user:
        return None
    if _hash_password(password, user.password_salt) != user.password_hash:
        return None
    return user


def get_user(user_id: str) -> User | None:
    return _users_by_id.get(user_id)


def update_profile(
    user_id: str,
    *,
    display_name: str | None = None,
    main_cv: str | None = None,
    life_story: str | None = None,
) -> User | None:
    user = _users_by_id.get(user_id)
    if not user:
        return None
    if display_name is not None:
        user.display_name = display_name.strip() or user.display_name
    if main_cv is not None:
        user.main_cv = main_cv.strip()
    if life_story is not None:
        user.life_story = life_story.strip()
    return user


SESSION_KEY = "user_id"


def session_user_id(request: Request) -> str | None:
    return request.session.get(SESSION_KEY)


def set_session_user(request: Request, user_id: str) -> None:
    request.session[SESSION_KEY] = user_id


def clear_session_user(request: Request) -> None:
    request.session.pop(SESSION_KEY, None)


def user_from_request(request: Request) -> User | None:
    uid = session_user_id(request)
    if not uid:
        return None
    return get_user(uid)


def get_user_by_reqme_token(token: str) -> User | None:
    uid = _reqme_token_to_user.get(token)
    if not uid:
        return None
    return get_user(uid)


def rotate_reqme_token(user_id: str) -> str | None:
    user = get_user(user_id)
    if not user:
        return None
    _reqme_token_to_user.pop(user.reqme_token, None)
    nt = secrets.token_urlsafe(12)
    user.reqme_token = nt
    _reqme_token_to_user[nt] = user_id
    return nt
