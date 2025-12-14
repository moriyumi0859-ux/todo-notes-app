from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Optional, Literal, Any, Dict
import uuid

Category = Literal["private", "work", "shopping"]

def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

@dataclass
class Task:
    id: str
    title: str
    category: Category
    done: bool = False
    due_date: Optional[str] = None      # YYYY-MM-DD
    due_time: Optional[str] = None      # HH:MM ← ★これが追加点
    notes: str = ""
    created_at: str = _now_iso()

    @staticmethod
    def new(
        title: str,
        category: Category,
        due_date: Optional[str],
        due_time: Optional[str],
        notes: str
    ) -> "Task":
        return Task(
            id=str(uuid.uuid4()),
            title=title.strip(),
            category=category,
            due_date=due_date,
            due_time=due_time,           # ← ★ここで保存される
            notes=notes.strip(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Memo:
    id: str
    text: str
    created_at: str = _now_iso()
    pinned: bool = False

    @staticmethod
    def new(text: str) -> "Memo":
        return Memo(id=str(uuid.uuid4()), text=text.strip())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
