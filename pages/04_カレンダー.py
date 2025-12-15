import streamlit as st
import base64
from pathlib import Path

from utils.ui import page_setup
from streamlit_calendar import calendar

# -----------------------------
# 0) 共通レイアウト（背景/カード/サイドバー等）
# -----------------------------
page_setup()

st.header("📅 カレンダー（期限日ベース）")

# -----------------------------
# 1) カレンダー周りのCanva装飾（右上に重ねる）
#    ※ home背景は page_setup() が担当
# -----------------------------
def calendar_decorate(image_filename: str):
    root = Path(__file__).resolve().parents[1]      # repo root
    img_path = root / "assets" / image_filename
    b64 = base64.b64encode(img_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        .calendar-wrap {{
            position: relative;
            padding: 28px;
            margin-top: 12px;
            border-radius: 22px;
            background-color: rgba(255,255,255,0.88);
        }}
        .calendar-wrap::after {{
            content: "";
            position: absolute;
            top: 10px;
            right: 10px;
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

# Canvaの装飾画像（assets/bg_calendar.png を想定）
calendar_decorate("bg_calendar.png")

# -----------------------------
# 2) tasks → events（期限日があるタスクだけ）
# -----------------------------
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []
for t in tasks:
    due = t.get("due_date")     # 例: "2025-12-20"
    title = t.get("title")
    if due and title:
        # 完了タスクを見分けたい場合（doneキーがある想定）
        prefix = "✅ " if t.get("done") else "📝 "
        events.append({"title": prefix + title, "start": due, "allDay": True})

# -----------------------------
# 3) カレンダー表示
# -----------------------------
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 720,
}

st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)
calendar(events=events, options=options, key="todo_calendar")
st.markdown("</div>", unsafe_allow_html=True)
