import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

page_setup()
st.header("📅 カレンダー（期限日ベース）")

# -----------------------------
# 1) tasks → events（期限日があるものだけ）
# -----------------------------
ttasks = st.session_state.get("data", {}).get("tasks", [])
events = []

COLOR_MAP = {
    "work":     {"color": "#1976d2"},  # 青
    "private":  {"color": "#2e7d32"},  # 緑
    "shopping": {"color": "#c62828"},  # 赤
}

LABEL_MAP = {
    "work": "💼",
    "private": "🏠",
    "shopping": "🛒",
}

for t in tasks:
    due = t.get("due_date")   # "YYYY-MM-DD"
    title = t.get("title")
    cat = t.get("category")

    if not (due and title):
        continue

    # 祝日/土日背景イベントと区別しやすいように「通常イベント」に色を付ける
    style = COLOR_MAP.get(cat, {"color": "#455a64"})  # 未知カテゴリはグレー
    icon = LABEL_MAP.get(cat, "📝")

    events.append({
        "title": f"{icon} {title}",
        "start": due,
        "allDay": True,
        **style,   # ←ここで色が効く
    })

# -----------------------------
# 2) 土日（繰り返し背景イベント：見やすく濃く）
# -----------------------------
events.append({
    "daysOfWeek": [0],  # 日曜
    "display": "background",
    "backgroundColor": "rgba(229,57,53,0.16)",  # ←濃く
})
events.append({
    "daysOfWeek": [6],  # 土曜
    "display": "background",
    "backgroundColor": "rgba(30,136,229,0.16)",  # ←濃く
})

# -----------------------------
# 3) 祝日（今年±1年分：年をまたいでも出る）
#    ※ 土日より “少し濃く” して区別
# -----------------------------
today = dt.date.today()
for y in [today.year - 1, today.year, today.year + 1]:
    for d, _name in jpholiday.year_holidays(y):
        events.append({
            "title": "holiday",
            "start": d.isoformat(),
            "allDay": True,
            "display": "background",
            "backgroundColor": "rgba(229,57,53,0.24)",  # ←土日より濃く
        })

# -----------------------------
# 4) カレンダー表示（サイズ固定）
# -----------------------------
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,  # ← 固定（お好みで 800〜1000）
    "headerToolbar": {
        "left": "title",
        "center": "",
        "right": "today prev,next",
    },
}

calendar(events=events, options=options, key="todo_calendar")
