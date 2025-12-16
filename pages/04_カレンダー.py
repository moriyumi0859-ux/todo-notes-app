import streamlit as st
import datetime as dt
import jpholiday
from utils.ui import page_setup
from streamlit_calendar import calendar

page_setup()
st.header("📅 カレンダー")

# ▶ 横幅（Streamlit本体側）
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
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []  # ← 必ず calendar() より前に定義！

COLOR_MAP = {
    "work": {"backgroundColor": "rgba(25,118,210,0.22)", "borderColor": "#1976d2", "textColor": "#0d47a1"},
    "private": {"backgroundColor": "rgba(46,125,50,0.22)", "borderColor": "#2e7d32", "textColor": "#1b5e20"},
    # shopping は CSS で完全に消すので、ここは最低限でもOK
    "shopping": {"backgroundColor": "transparent", "borderColor": "transparent", "textColor": "#b71c1c"},
}
LABEL_MAP = {"work": "💼", "private": "🏠", "shopping": "🛒"}
DEFAULT_STYLE = {"backgroundColor": "rgba(69,90,100,0.22)", "borderColor": "#455a64", "textColor": "#263238"}

for t in tasks:
    due = t.get("due_date")         # "2025-12-15"
    due_time = t.get("due_time")    # "14:30" みたいに保存している想定（無ければ None）
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

    # ★カテゴリ別にクラス名を付ける（CSSで狙い撃ちできる）
    class_names = [f"cat-{cat}"] if cat else ["cat-unknown"]

    events.append({
        "title": f"{icon} {title}",
        "start": start_dt,
        "allDay": all_day,
        "classNames": class_names,
        **style,
    })

# =============================
# 2) 土日背景
# =============================
events.append({"daysOfWeek": [0], "display": "background", "backgroundColor": "rgba(229,57,53,0.18)"})
events.append({"daysOfWeek": [6], "display": "background", "backgroundColor": "rgba(30,136,229,0.18)"})

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
            "backgroundColor": "rgba(229,57,53,0.28)",
        })

# =============================
# 4) 表示オプション
# =============================
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},
}

# ▶ カレンダー内部に効かせるCSS（ここ重要）
custom_css = """
/* =================================
   ヘッダータイトル
   ================================= */
.fc .fc-toolbar-title {
  font-size: 2.5em;
  margin: 15px;
  margin-top: 20px;
}

/* ヘッダー全体の余白 */
.fc .fc-toolbar.fc-header-toolbar {
  margin-bottom: 0em;
}

/* =================================
   カレンダーボタン完全統一
   ================================= */

/* 共通（today / prev / next すべて） */
.fc .fc-button {
  background-color: #d32f2f !important;
  border-color: #d32f2f !important;
  color: #ffffff !important;
  box-shadow: 0 3px 6px rgba(0,0,0,0.25);
  transition: all 0.15s ease;
}

/* hover */
.fc .fc-button:hover {
  background-color: #c62828 !important;
  border-color: #c62828 !important;
}

/* 押している瞬間（分かりやすい） */
.fc .fc-button:active {
  background-color: #7f0000 !important;
  border-color: #7f0000 !important;
  transform: translateY(2px);
  box-shadow: inset 0 3px 6px rgba(0,0,0,0.35);
}

/* 選択中（today / 表示中） */
.fc .fc-button.fc-button-active,
.fc .fc-button.fc-today-button.fc-button-active {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.25);
}

/* today ボタン（色ブレ防止） */
.fc .fc-button.fc-today-button {
  background-color: #d32f2f !important;
  border-color: #d32f2f !important;
  color: #ffffff !important;
}

/* 無効状態（today が押せない時） */
.fc .fc-button:disabled {
  background-color: #ef9a9a !important;
  border-color: #ef9a9a !important;
  color: #ffffff !important;
  opacity: 1 !important;
  box-shadow: none;
}

/* =================================
   shopping を“文字だけ”にする
   ================================= */

/* イベント本体 */
.fc .cat-shopping.fc-event,
.fc .cat-shopping .fc-event-main,
.fc .cat-shopping .fc-event-main-frame {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
}

/* 月表示用の補正 */
.fc .fc-daygrid-event.cat-shopping {
  background: transparent !important;
  border: none !important;
}

/* 文字色だけ残す */
.fc .cat-shopping .fc-event-title,
.fc .cat-shopping .fc-event-time {
  color: #b71c1c !important;
  font-weight: 700;
}

/* =================================
   右側ボタン位置調整
   ================================= */
.fc .fc-toolbar-chunk:last-child {
  margin-right: 30px;
}
"""

calendar(events=events, options=options, custom_css=custom_css, key="todo_calendar")


