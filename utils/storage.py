from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

from utils.constants import DEFAULT_BG_THEME

# ✅ このファイル(utils/storage.py)から見た「プロジェクト直下」を固定
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "app_data.json"

DEFAULT_DATA: Dict[str, Any] = {
    "tasks": [],
    "memos": [],
    "settings": {"bg_theme": DEFAULT_BG_THEME},
}

def load_data(path: Path = DATA_PATH) -> Dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        save_data(DEFAULT_DATA, path)
        return dict(DEFAULT_DATA)

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        data.setdefault("tasks", [])
        data.setdefault("memos", [])
        data.setdefault("settings", {})
        data["settings"].setdefault("bg_theme", DEFAULT_BG_THEME)

        # ✅ 互換性：due_time がない古いタスクにも対応
        for t in data.get("tasks", []):
            t.setdefault("due_time", None)

        return data
    except Exception:
        save_data(DEFAULT_DATA, path)
        return dict(DEFAULT_DATA)

def save_data(data: Dict[str, Any], path: Path = DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
