import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="カレンダー", layout="wide")

def set_calendar_bg(filename: str):
    root = Path(__file__).resolve().parents[1]
    img_path = root / "assets" / filename

    # デバッグ（1回だけ入れて確認）
    st.write("bg path:", str(img_path))
    st.write("exists:", img_path.exists())

    b64 = base64.b64encode(img_path.read_bytes()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
        section[data-testid="stMain"] > div {{
            background: rgba(255,255,255,0.82);
            border-radius: 16px;
            padding: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_calendar_bg("bg_calendar.png")

st.title("📅 カレンダー（期限日ベース）")

from streamlit_calendar import calendar  # ← ここでimport（遅延import）

events = [
    {"title": "企画書提出", "start": "2025-12-20", "allDay": True},
    {"title": "会議資料", "start": "2025-12-18", "allDay": True},
]

options = {"initialView": "dayGridMonth", "locale": "ja", "height": 700}
calendar(events=events, options=options, key="todo_calendar")
