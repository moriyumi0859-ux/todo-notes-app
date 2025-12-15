import sys
from pathlib import Path
import streamlit as st
import base64

# ★ pages/ の1つ上（リポジトリ直下）を import パスに追加
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.style import apply_global_styles

# 1) これが最初＆1回だけ
st.set_page_config(page_title="カレンダー", layout="wide")

# 2) homeと同じ背景テーマ
bg_theme = st.session_state.get("data", {}).get("settings", {}).get("bg_theme", "home")
apply_global_styles(bg_theme)



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
