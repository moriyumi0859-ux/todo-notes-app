import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

page_setup()
st.header("📅 カレンダー（期限日ベース）")

# --- 土日を見分けやすく（文字色＋うっすら背景）---
# ※ FullCalendar の中だけに効かせる（他のUIに影響しない）
st.markdown(
    """
    <style>
    /* 日曜 */
    .fc .fc-daygrid-day.fc-day-sun{
      background: rgba(229,57,53,0.06) !important;
    }
    .fc .fc-daygrid-day.fc-day-sun .fc-daygrid-day-number{
      color: #e53935 !important;
      font-weight: 700 !important;
    }

    /* 土曜 */
    .fc .fc-daygrid-day.fc-day-sat{
      background: rgba(30,136,229,0.06) !important;
    }
    .fc .fc-daygrid-day.fc-day-sat .fc-daygrid-day-number{
      color: #1e88e5 !important;
      font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# tasks → events
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []
for t in tasks:
    due = t.get("due_date")   # "YYYY-MM-DD"
    title = t.get("title")
    if due and title:
        events.append({"title": title, "start": due, "allDay": True})

# 祝日（薄赤背景）
year = dt.date.today().year
for d, _name in jpholiday.year_holidays(year):
    events.append({
        "title": "holiday",
        "start": d.isoformat(),
        "allDay": True,
        "display": "background",
        "backgroundColor": "rgba(229,57,53,0.12)",
    })

# ✅ カレンダーが小さくならない最重要ポイント：height を固定
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},
}

calendar(events=events, options=options, key="todo_calendar")
