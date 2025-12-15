import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

# =========================
# 0) 共通レイアウト
# =========================
page_setup()

# =========================
# 1) カレンダーページ専用CSS
#    ・上の細長い白カードを消す
#    ・横幅を広げる
#    ・曜日色／今日強調
# =========================
st.markdown(
    """
    <style>
    /* =========================
       1) 横に細長い白いカードの正体（外側カード）を消す
       ========================= */
    [data-testid="stMainBlockContainer"]{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding-top: 0 !important;
    }

    /* page_setup由来のカード（環境によってはこっちが効く） */
    .block-container{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        margin-top: 0 !important;
    }

    /* =========================
       2) カレンダーのカードを「完全な白」にする（不透明）
       ========================= */
    .calendar-wrap{
        background: #ffffff !important;      /* ← 半透明やめて真っ白 */
        border-radius: 22px;
        padding: 24px;
        margin-top: 12px;
        box-shadow: 0 14px 40px rgba(0,0,0,0.16);  /* 影を少し綺麗に */
    }

    /* FullCalendar本体も透けないように（念のため） */
    .calendar-wrap .fc{
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("📅 カレンダー（期限日ベース）")

# =========================
# 2) tasks → events
# =========================
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

for t in tasks:
    due = t.get("due_date")
    title = t.get("title")
    if due and title:
        prefix = "✅ " if t.get("done") else ""
        events.append({
            "title": prefix + title,
            "start": due,
            "allDay": True,
        })

# =========================
# 3) 祝日（日本の一般的な見え方）
# =========================
today = dt.date.today()
year = today.year

for d, name in jpholiday.year_holidays(year):
    events.append({
        "title": name,
        "start": d.isoformat(),
        "allDay": True,
        "display": "background",
        "backgroundColor": "rgba(229,57,53,0.10)",
    })

# =========================
# 4) カレンダー表示
# =========================
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
}

st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)
calendar(events=events, options=options, key="todo_calendar")
st.markdown('</div>', unsafe_allow_html=True)
