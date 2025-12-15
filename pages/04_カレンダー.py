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
    /* --- 外側の細長い白カードを消す --- */
    section[data-testid="stMain"] .block-container{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
        margin-top: 0 !important;
        max-width: 1400px !important;
    }

    /* --- 曜日ヘッダー --- */
    .fc-col-header-cell.fc-day-sun,
    .fc-col-header-cell.fc-day-sun a{
        color: #e53935 !important;
        font-weight: 700;
    }

    .fc-col-header-cell.fc-day-sat,
    .fc-col-header-cell.fc-day-sat a{
        color: #1e88e5 !important;
        font-weight: 700;
    }

    /* --- 日付の数字も色分け --- */
    .fc-daygrid-day.fc-day-sun .fc-daygrid-day-number{
        color: #e53935;
    }
    .fc-daygrid-day.fc-day-sat .fc-daygrid-day-number{
        color: #1e88e5;
    }

    /* --- 今日をうっすら強調 --- */
    .fc-daygrid-day.fc-day-today{
        background: rgba(255, 193, 7, 0.12) !important;
    }

    /* --- カレンダー本体の白カード --- */
    .calendar-wrap{
        background: rgba(255,255,255,0.88);
        border-radius: 22px;
        padding: 24px;
        margin-top: 12px;
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
