import streamlit as st
import base64
from streamlit_calendar import calendar

# ===== ① Canva背景をこのページだけに適用 =====
# set_page_configは「最初」に書くのが鉄則
st.set_page_config(page_title="カレンダー", layout="wide")

def set_calendar_bg(filename: str):
    root = Path(__file__).resolve().parents[1]   # pages/ の1つ上＝リポジトリルート想定
    img_path = root / "assets" / filename

    b64 = base64.b64encode(img_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        /* Streamlitのバージョン差に強い指定 */
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}

        /* 上部バーが背景を隠す場合の対策 */
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        /* コンテンツに白い半透明面を敷いて読みやすく */
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

# ===== ② ここから通常のページ処理 =====
st.title("📅 カレンダー（期限日ベース）")

events = [
    {"title": "企画書提出", "start": "2025-12-20", "allDay": True},
    {"title": "会議資料", "start": "2025-12-18", "allDay": True},
]

options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 700,
}

calendar(events=events, options=options, key="todo_calendar")
