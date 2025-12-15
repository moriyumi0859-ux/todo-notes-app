import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

page_setup()
st.header("📅 カレンダー（期限日ベース）")

# tasks → events（期限日があるものだけ）
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

for t in tasks:
    due = t.get("due_date")   # "YYYY-MM-DD"
    title = t.get("title")
    if due and title:
        events.append({
            "title": title,
            "start": due,
            "allDay": True,
        })

# 祝日（薄赤の背景）
year = dt.date.today().year
for d, _name in jpholiday.year_holidays(year):
    events.append({
        "title": "holiday",
        "start": d.isoformat(),
        "allDay": True,
        "display": "background",
        "backgroundColor": "rgba(229,57,53,0.10)",
    })

options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},
}

calendar(events=events, options=options, key="todo_calendar")

