import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="カレンダー", layout="wide")

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

calendar_decorate("bg_calendar.png")

# ここから「表示領域」
st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)

from streamlit_calendar import calendar

events = []

tasks = []  # ← あなたのDB/JSON/セッションから取得したtasksに置き換え

events = []
for t in tasks:
    due = t.get("due_date")
    title = t.get("title")
    if due and title:
        events.append({"title": title, "start": due, "allDay": True})

options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 700,
}

calendar(events=events, options=options, key="todo_calendar")

st.markdown("</div>", unsafe_allow_html=True)