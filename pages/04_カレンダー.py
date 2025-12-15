import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar
from datetime import datetime

# =============================
# 0) 共通レイアウト
# =============================
page_setup()
st.header("📅 カレンダー（期限日ベース）")

custom_css = """
/* ▶ カレンダーのタイトル */
.fc .fc-toolbar-title {
  font-size: 2.5em;
  margin: 15px;
}

/* ▶ カレンダーのボタン */
.fc .fc-button {
  border-radius: 0px;
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  margin: 8px;
  text-transform: none;
}
"""

calendar(events=events, options=options, custom_css=custom_css, key="todo_calendar")


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
# 1) tasks → events（カテゴリ色分け）
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
    due = t.get("due_date")
    title = t.get("title")
    cat = t.get("category")

    if not (due and title):
        continue

    style = COLOR_MAP.get(cat, DEFAULT_STYLE)
    icon = LABEL_MAP.get(cat, "📝")

    events.append({
        "title": f"{icon} {title}",
        "start": due,
        "allDay": True,
        **style,
    })

# =============================
# 2) 土日（背景：少し濃い）
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
# 4) カレンダー表示
# =============================
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
    "headerToolbar": {
        "left": "title",
        "center": "",
        "right": "today prev,next",
    },
}

calendar(events=events, options=options, key="todo_calendar")
