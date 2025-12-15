import streamlit as st
import datetime as dt
import jpholiday
from utils.ui import page_setup
from streamlit_calendar import calendar
from datetime import datetime

page_setup()
st.header("📅 カレンダー（期限日ベース）")

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
    "shopping": {
        "backgroundColor": "transparent",  # ← 背景を消す
        "borderColor": "transparent",      # ← 枠を消す
        "textColor": "#b71c1c",            # ← 文字色だけ残す
    },
}

LABEL_MAP = {"work": "💼", "private": "🏠", "shopping": "🛒"}
DEFAULT_STYLE = {"backgroundColor": "rgba(69,90,100,0.22)", "borderColor": "#455a64", "textColor": "#263238"}

from datetime import datetime

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

    events.append({
        "title": f"{icon} {title}",
        "start": start_dt,
        "allDay": all_day,
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
/* ===== ヘッダータイトル ===== */
.fc .fc-toolbar-title {
  font-size: 2.5em;
  margin: 15px;
  margin-top: 20px;   /* タイトルを下に */
}

/* ヘッダー全体の余白 */
.fc .fc-toolbar.fc-header-toolbar {
  margin-bottom: 0em;
}

/* ===== カレンダーボタン ===== */
.fc .fc-button:hover {
  transform: translateY(-1px);
  box-shadow:
    0 6px 14px rgba(0,0,0,0.18),
    inset 0 1px 0 rgba(255,255,255,0.95);
}

.fc .fc-button:active {
  transform: translateY(1px);
  box-shadow:
    0 2px 6px rgba(0,0,0,0.15),
    inset 0 2px 4px rgba(0,0,0,0.15);
}

/* ▶ 右側のボタン群を左へ寄せる */
.fc .fc-toolbar-chunk:last-child {
  margin-right: 30px;
}

"""


calendar(events=events, options=options, custom_css=custom_css, key="todo_calendar")
