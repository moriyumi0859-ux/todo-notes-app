from utils.ui import page_setup
from streamlit_calendar import calendar
import streamlit as st
import base64
from pathlib import Path

page_setup()

# ✅ カレンダーページだけ「中央カードの幅」を広げる（見やすくする）
st.markdown(
    """
    <style>
    section[data-testid="stMain"] .block-container{
        max-width: 1400px !important;   /* お好みで 1200〜1600 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("📅 カレンダー（期限日ベース）")

def calendar_decorate(image_filename: str):
    root = Path(__file__).resolve().parents[1]
    img_path = root / "assets" / image_filename
    b64 = base64.b64encode(img_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        .calendar-wrap {{
            position: relative;
            padding: 22px;
            margin-top: 12px;
            border-radius: 22px;
            background-color: rgba(255,255,255,0.88);
            /* もし枠内にも薄く背景を入れたいなら（任意） */
            /* background-image: url("data:image/png;base64,{b64}");
               background-size: contain;
               background-repeat: no-repeat;
               background-position: top right; */
        }}
        /* ✅ これが「小さい白いカード＋小さい別カレンダー」の犯人なので削除！ */
        </style>
        """,
        unsafe_allow_html=True,
    )

calendar_decorate("bg_calendar.png")

st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)

tasks = st.session_state.get("data", {}).get("tasks", [])
events = []
for t in tasks:
    due = t.get("due_date")
    title = t.get("title")
    if due and title:
        events.append({"title": title, "start": due, "allDay": True})

options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,   # ✅ 大きく（お好みで 800〜1000）
}

calendar(events=events, options=options, key="todo_calendar")

st.markdown("</div>", unsafe_allow_html=True)
