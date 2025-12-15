import streamlit as st
import base64
from pathlib import Path
import importlib.util

# ===== style.py を「パス指定」で確実に読み込む =====
ROOT = Path(__file__).resolve().parents[1]                 # /mount/src/todo-notes-app
STYLE_PATH = ROOT / "utils" / "style.py"

spec = importlib.util.spec_from_file_location("app_style", STYLE_PATH)
app_style = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_style)

apply_global_styles = app_style.apply_global_styles




def calendar_decorate(image_filename: str):
    root = Path(__file__).resolve().parents[1]
    img_path = root / "assets" / image_filename
    b64 = base64.b64encode(img_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        .calendar-wrap {{
            position: relative;
            padding: 32px;
            margin-top: 16px;
            border-radius: 22px;
            background-color: rgba(255,255,255,0.88);
        }}
        .calendar-wrap::after {{
            content: "";
            position: absolute;
            top: 12px;
            right: 12px;
            width: 260px;
            height: 260px;
            background-image: url("data:image/png;base64,{b64}");
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.9;
            pointer-events: none;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("📅 カレンダー（期限日ベース）")

# カレンダー用の装飾（右上のCanvaパーツ）
calendar_decorate("bg_calendar.png")

# ここから表示領域
st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)

from streamlit_calendar import calendar

# --- ここは後であなたの実データに置き換え ---
tasks = []  # 例: load_tasks() など
events = []
for t in tasks:
    due = t.get("due_date")
    title = t.get("title")
    if due and title:
        events.append({"title": title, "start": due, "allDay": True})
# ------------------------------------------

options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 700,
}

calendar(events=events, options=options, key="todo_calendar")

st.markdown("</div>", unsafe_allow_html=True)
