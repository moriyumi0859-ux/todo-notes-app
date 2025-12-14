# utils/theme.py
from __future__ import annotations
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # to_do_app/

BG_MAP = {
    "ボタニカル1": ROOT / "assets/backgrounds/botanical1.png",
    "ボタニカル2": ROOT / "assets/backgrounds/botanical2.png",
    "ダマスク":     ROOT / "assets/backgrounds/damask.png",
    "猫":           ROOT / "assets/backgrounds/cat.png",
    "犬":           ROOT / "assets/backgrounds/dog.png",
    "木目調":       ROOT / "assets/backgrounds/wood.png",
    "大理石":       ROOT / "assets/backgrounds/marble.png",
    "バリ島":   ROOT / "assets/backgrounds/bali.png",
    "グラフィック":   ROOT / "assets/backgrounds/graphic.png",
}

def img_to_base64(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode("utf-8")
