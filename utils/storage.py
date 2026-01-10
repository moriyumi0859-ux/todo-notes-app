from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

from utils.constants import DEFAULT_BG_THEME

# プロジェクト直下のパスを固定
ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DATA: Dict[str, Any] = {
    "tasks": [],
    "memos": [],
    "settings": {"bg_theme": DEFAULT_BG_THEME},
}

def get_user_data_path(username: str) -> Path:
    """ユーザー名に基づいたファイルパスを取得（安全なファイル名に変換）"""
    # 記号などを排除してファイル名として安全な文字列にする
    safe_username = "".join([c for c in username if c.isalnum()])
    if not safe_username:
        safe_username = "default"
    return ROOT / "data" / f"user_{safe_username}.json"

def load_data(username: str = "default") -> Dict[str, Any]:
    """指定されたユーザーのデータを読み込む"""
    path = get_user_data_path(username)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        save_data(DEFAULT_DATA, username)
        return dict(DEFAULT_DATA)

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # データの整合性を保つための初期化設定
        data.setdefault("tasks", [])
        data.setdefault("memos", [])
        data.setdefault("settings", {})
        data["settings"].setdefault("bg_theme", DEFAULT_BG_THEME)

        # 互換性：due_time がない古いタスクにも対応
        for t in data.get("tasks", []):
            t.setdefault("due_time", None)

        return data
    except Exception:
        # 読み込み失敗時は初期データを保存して返す
        save_data(DEFAULT_DATA, username)
        return dict(DEFAULT_DATA)

def save_data(data: Dict[str, Any], username: str = "default") -> None:
    """指定されたユーザーのデータを保存する"""
    path = get_user_data_path(username)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)