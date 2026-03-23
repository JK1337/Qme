"""Play-to-learn credits, spendable balance, and certificates — in-memory demo."""

from __future__ import annotations

from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

REWRITE_COST = 15


@dataclass
class TrainingModule:
    id: str
    title: str
    credits: int
    certificate: str


@dataclass
class UserProgress:
    user_id: str
    completed_module_ids: set[str] = field(default_factory=set)

    def total_credits(self, catalog: list[TrainingModule]) -> int:
        by_id = {m.id: m for m in catalog}
        return sum(by_id[mid].credits for mid in self.completed_module_ids if mid in by_id)


DEMO_MODULES: list[TrainingModule] = [
    TrainingModule(
        id="mod-interview",
        title="Interview storytelling",
        credits=50,
        certificate="Qme Storytelling Basics",
    ),
    TrainingModule(
        id="mod-salary",
        title="Negotiation fundamentals",
        credits=40,
        certificate="Qme Negotiation Ready",
    ),
    TrainingModule(
        id="mod-brand",
        title="Personal brand & reQme",
        credits=60,
        certificate="Qme Visible Profile",
    ),
]

_progress: dict[str, UserProgress] = {}
_spent: dict[str, int] = {}


def get_catalog() -> list[TrainingModule]:
    return DEMO_MODULES


def progress_key(session: MutableMapping[str, Any], logged_in_user_id: str | None) -> str:
    if logged_in_user_id:
        return f"u:{logged_in_user_id}"
    gid = session.get("guest_learn_id")
    if not gid:
        gid = uuid4().hex
        session["guest_learn_id"] = gid
    return f"g:{gid}"


def _get_or_create_progress(key: str) -> UserProgress:
    if key not in _progress:
        _progress[key] = UserProgress(user_id=key, completed_module_ids=set())
    return _progress[key]


def get_progress(session: MutableMapping[str, Any], logged_in_user_id: str | None) -> UserProgress:
    return _get_or_create_progress(progress_key(session, logged_in_user_id))


def progress_for_logged_user_id(user_id: str) -> UserProgress:
    """Progress for a registered user (e.g. public reQme) without using the request session."""
    return _get_or_create_progress(f"u:{user_id}")


def complete_module(
    session: MutableMapping[str, Any],
    logged_in_user_id: str | None,
    module_id: str,
) -> UserProgress:
    if not any(m.id == module_id for m in DEMO_MODULES):
        return get_progress(session, logged_in_user_id)
    prog = _get_or_create_progress(progress_key(session, logged_in_user_id))
    prog.completed_module_ids.add(module_id)
    return prog


def earned_credits(key: str, catalog: list[TrainingModule] | None = None) -> int:
    catalog = catalog or DEMO_MODULES
    return _get_or_create_progress(key).total_credits(catalog)


def balance_for_key(key: str, catalog: list[TrainingModule] | None = None) -> int:
    catalog = catalog or DEMO_MODULES
    e = earned_credits(key, catalog)
    s = _spent.get(key, 0)
    return max(0, e - s)


def balance_for_session(session: MutableMapping[str, Any], logged_in_user_id: str | None) -> int:
    return balance_for_key(progress_key(session, logged_in_user_id))


def try_spend(session: MutableMapping[str, Any], logged_in_user_id: str | None, amount: int) -> bool:
    """Spend credits; only meaningful for logged-in users (guests do not pay for rewrites)."""
    if not logged_in_user_id or amount <= 0:
        return True
    key = f"u:{logged_in_user_id}"
    catalog = DEMO_MODULES
    if balance_for_key(key, catalog) < amount:
        return False
    _spent[key] = _spent.get(key, 0) + amount
    return True


def certificates_for_progress(prog: UserProgress, catalog: list[TrainingModule] | None = None) -> list[str]:
    catalog = catalog or DEMO_MODULES
    by_id = {m.id: m for m in catalog}
    return [by_id[mid].certificate for mid in sorted(prog.completed_module_ids) if mid in by_id]


def migrate_guest_to_user(session: MutableMapping[str, Any], user_id: str) -> None:
    gid = session.pop("guest_learn_id", None)
    if not gid:
        return
    gkey = f"g:{gid}"
    ukey = f"u:{user_id}"
    guest_prog = _progress.pop(gkey, None)
    if not guest_prog:
        return
    user_prog = _get_or_create_progress(ukey)
    user_prog.completed_module_ids |= guest_prog.completed_module_ids
    g_spent = _spent.pop(gkey, 0)
    if g_spent:
        _spent[ukey] = _spent.get(ukey, 0) + g_spent


def new_share_token() -> str:
    return uuid4().hex[:12]
