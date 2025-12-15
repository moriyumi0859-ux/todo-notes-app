import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

# =============================
# 0) 共通レイアウト
# =============================
page_setup()
st.header("📅 カレンダー（期限日ベース）")

# ▶ 横幅を広く固定（狭くならない対策）
st.markdown(
    """
    <style>
    section[data-testid="stMain"] .block-container{
        max-width: 1400px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================
# 1) tasks → events（カテゴリ色分け + 時刻対応）
# =============================
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

# ▶ すべて「同じ薄さ（0.22）」で統一
COLOR_MAP = {
    "work": {
        "backgroundColor": "rgba(25,118,210,0.22)",
        "borderColor": "#1976d2",
        "textColor": "#0d47a1",
    },
    "private": {
        "backgroundColor": "rgba(46,125,50,0.22)",
        "borderColor": "#2e7d32",
        "textColor": "#1b5e20",
    },
    "shopping": {
        "backgroundColor": "rgba(198,40,40,0.22)",
        "borderColor": "#c62828",
        "textColor": "#b71c1c",
    },
}

LABEL_MAP = {
    "work": "💼",
    "private": "🏠",
    "shopping": "🛒",
}

DEFAULT_STYLE = {
    "backgroundColor": "rgba(69,90,100,0.22)",
    "borderColor": "#455a64",
    "textColor": "#263238",
}

for t in tasks:
    due = t.get("due_date")          # "YYYY-MM-DD"
    due_time = t.get("due_time")     # "HH:MM"（無ければ None）
    title = t.get("title")
    cat = t.get("category")

    if not (due and title):
        continue

    style = COLOR_MAP.get(cat, DEFAULT_STYLE)
    icon = LABEL_MAP.get(cat, "📝")

    # ✅ 時刻がある場合は start を ISO datetime に
    if due_time:
        start = f"{due}T{due_time}:00"
        all_day = False
    else:
        start = due
        all_day = True

    events.append({
        "title": f"{icon} {title}",
        "start": start,
        "allDay": all_day,
        "extendedProps": {"due_time": due_time, "category": cat},
        **style,
    })

# =============================
# 2) 土日（背景）
# =============================
events.append({
    "daysOfWeek": [0],  # 日曜
    "display": "background",
    "backgroundColor": "rgba(229,57,53,0.18)",
})
events.append({
    "daysOfWeek": [6],  # 土曜
    "display": "background",
    "backgroundColor": "rgba(30,136,229,0.18)",
})

# =============================
# 3) 祝日（今年±1年）
# =============================
today = dt.date.today()
for y in [today.year - 1, today.year, today.year + 1]:
    for d, _ in jpholiday.year_holidays(y):
        events.append({
            "title": "holiday",
            "start": d.isoformat(),
            "allDay": True,
            "display": "background",
            "backgroundColor": "rgba(229,57,53,0.28)",  # 土日より濃く
        })

# =============================
# 4) カレンダー表示（クリックで詳細を表示）
# =============================
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},
}

cal = calendar(
    events=events,
    options=options,
    callbacks=["eventClick"],
    key="todo_calendar",
)

# =============================
# 5) クリックした用事の「時刻」を表示
# =============================
clicked = (cal or {}).get("eventClick")
if clicked:
    ev = clicked.get("event", {})
    title = ev.get("title", "")
    start = ev.get("start", "")  # "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS"

    if isinstance(start, str) and "T" in start:
        time_str = start.split("T", 1)[1][:5]  # HH:MM
        st.info(f"🕒 {title}：{time_str}")
    else:
        st.info(f"📌 {title}：終日")
