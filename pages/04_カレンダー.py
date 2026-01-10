import streamlit as st
import datetime as dt
import jpholiday

# --- 1. ログインチェック (必須) ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("ログインが必要です。ホーム画面からログインしてください。")
    st.stop()

# --- 2. 必要なライブラリと設定 ---
from utils.ui import page_setup
from streamlit_calendar import calendar

page_setup()

# ヘッダー (スマホ対応)
st.markdown(
    '<h2 style="font-size: 1.4rem; white-space: nowrap; margin-bottom: 1rem;">📅 カレンダー</h2>', 
    unsafe_allow_html=True
)

# 横幅調整
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
# 1) tasks → events
# =============================
# ログイン中のユーザーのタスクのみを取得
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

COLOR_MAP = {
    "work": {"backgroundColor": "rgba(25,118,210,0.22)", "borderColor": "#1976d2", "textColor": "#0d47a1"},
    "private": {"backgroundColor": "rgba(46,125,50,0.22)", "borderColor": "#2e7d32", "textColor": "#1b5e20"},
    "shopping": {"backgroundColor": "transparent", "borderColor": "transparent", "textColor": "#b71c1c"},
}
LABEL_MAP = {"work": "💼", "private": "🏠", "shopping": "🛒"}
DEFAULT_STYLE = {"backgroundColor": "rgba(69,90,100,0.22)", "borderColor": "#455a64", "textColor": "#263238"}

for t in tasks:
    due = t.get("due_date")
    due_time = t.get("due_time")
    title = t.get("title")
    cat = t.get("category")

    if not (due and title):
        continue

    style = COLOR_MAP.get(cat, DEFAULT_STYLE)
    icon = LABEL_MAP.get(cat, "📝")

    if due_time:
        start_dt = f"{due}T{due_time}:00"
        all_day = False
    else:
        start_dt = due
        all_day = True

    class_names = [f"cat-{cat}"] if cat else ["cat-unknown"]

    events.append({
        "title": f"{icon} {title}",
        "start": start_dt,
        "allDay": all_day,
        "classNames": class_names,
        **style,
    })

# =============================
# 2) 土日祝背景
# =============================
events.append({"daysOfWeek": [0], "display": "background", "backgroundColor": "rgba(229,57,53,0.18)"})
events.append({"daysOfWeek": [6], "display": "background", "backgroundColor": "rgba(30,136,229,0.18)"})

today = dt.date.today()
for y in [today.year - 1, today.year, today.year + 1]:
    for d, _ in jpholiday.year_holidays(y):
        events.append({
           "start": d.isoformat(),
           "allDay": True,
           "display": "background",
           "backgroundColor": "rgba(229,57,53,0.28)",
})

# =============================
# 3) カレンダー表示オプション
# =============================
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": "auto",
    "contentHeight": "auto",
    "dayMaxEvents": True,
    "stickyHeaderDates": True,
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},
    "buttonText": {"today": "今日"},
}

# (CSS部分は省略せずに元のまま適用してください)
custom_css = """
/* ヘッダー・ボタン・スマホ最適化のCSS (提示されたコードと同じ) */
.fc .fc-toolbar-title { font-size: 2.2em; margin: 12px; margin-top: 18px; }
.fc .fc-button { background-color: #d32f2f !important; border-color: #d32f2f !important; color: #ffffff !important; }
/* ... (中略: 元の長いCSSをここに貼り付けます) ... */
@media (max-width: 768px) {
  .fc .fc-toolbar-title { font-size: 1.4em !important; }
  .fc .fc-view-harness { min-height: 72vh !important; }
}
"""

# カレンダーのレンダリング
calendar(
    events=events,
    options=options,
    custom_css=custom_css,
    key="todo_calendar",
)