"""Learn-to-earn points — in-memory demo store; swap for DB later."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class TrainingModule:
    id: str
    title: str
    points: int
    certificate: str


@dataclass
class UserProgress:
    user_id: str
    completed_module_ids: set[str] = field(default_factory=set)

    def total_points(self, catalog: list[TrainingModule]) -> int:
        by_id = {m.id: m for m in catalog}
        return sum(by_id[mid].points for mid in self.completed_module_ids if mid in by_id)


DEMO_MODULES: list[TrainingModule] = [
    TrainingModule(
        id="mod-interview",
        title="Interview storytelling",
        points=50,
        certificate="Qme Storytelling Basics",
    ),
    TrainingModule(
        id="mod-salary",
        title="Negotiation fundamentals",
        points=40,
        certificate="Qme Negotiation Ready",
    ),
    TrainingModule(
        id="mod-brand",
        title="Personal brand & reQme",
        points=60,
        certificate="Qme Visible Profile",
    ),
]

# Single demo user for scaffold
_demo_progress = UserProgress(user_id="demo-user")


def get_catalog() -> list[TrainingModule]:
    return DEMO_MODULES


def get_progress() -> UserProgress:
    return _demo_progress


def complete_module(module_id: str) -> UserProgress:
    if any(m.id == module_id for m in DEMO_MODULES):
        _demo_progress.completed_module_ids.add(module_id)
    return _demo_progress


def new_share_token() -> str:
    return uuid4().hex[:12]
