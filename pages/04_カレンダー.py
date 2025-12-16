import streamlit as st
import datetime as dt
import jpholiday
from utils.ui import page_setup
from streamlit_calendar import calendar

page_setup()
st.header("📅 カレンダー")

# ▶ 横幅（PCは広く / スマホは自動的に狭く見える）
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
events = []

COLOR_MAP = {
    "work": {"backgroundColor": "rgba(25,118,210,0.22)", "borderColor": "#1976d2", "textColor": "#0d47a1"},
    "private": {"backgroundColor": "rgba(46,125,50,0.22)", "borderColor": "#2e7d32", "textColor": "#1b5e20"},
    "shopping": {"backgroundColor": "transparent", "borderColor": "transparent", "textColor": "#b71c1c"},
}
LABEL_MAP = {"work": "💼", "private": "🏠", "shopping": "🛒"}
DEFAULT_STYLE = {"backgroundColor": "rgba(69,90,100,0.22)", "borderColor": "#455a64", "textColor": "#263238"}

for t in tasks:
    due = t.get("due_date")         # "2025-12-15"
    due_time = t.get("due_time")    # "14:30" or None
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
            "title": "祝日",
            "start": d.isoformat(),
            "allDay": True,
            "display": "background",
            "backgroundColor": "rgba(229,57,53,0.28)",
        })

# =============================
# 4) 表示オプション（スマホで崩れにくい設定）
# =============================
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",

    # 高さは「固定」だとスマホで厳しいので auto 寄りに（効かない環境もあるためCSSでも補強）
    "height": "auto",
    "contentHeight": "auto",

    # 月表示をスマホで見やすく：予定が多い日は「+ more」に逃がす
    "dayMaxEvents": True,

    # タップしやすさ・表示安定
    "stickyHeaderDates": True,

    # ヘッダー（右側をコンパクトに）
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},

    # ボタン文言を短く（スマホで効く）
    "buttonText": {"today": "今日"},
}

# =============================
# 5) custom_css（PC + スマホ最適化）
# =============================
custom_css = """
/* =================================
   ヘッダータイトル
   ================================= */
.fc .fc-toolbar-title {
  font-size: 2.2em;
  margin: 12px;
  margin-top: 18px;
}

/* ヘッダー余白 */
.fc .fc-toolbar.fc-header-toolbar {
  margin-bottom: 0.2em;
}

/* =================================
   ボタン統一（全状態）
   ================================= */
.fc .fc-button {
  background-color: #d32f2f !important;
  border-color: #d32f2f !important;
  color: #ffffff !important;
  box-shadow: 0 3px 6px rgba(0,0,0,0.25);
  transition: all 0.15s ease;
}

.fc .fc-button:hover {
  background-color: #c62828 !important;
  border-color: #c62828 !important;
}

.fc .fc-button:active {
  background-color: #7f0000 !important;
  border-color: #7f0000 !important;
  transform: translateY(2px);
  box-shadow: inset 0 3px 6px rgba(0,0,0,0.35);
}

/* 選択中（押した後も分かる） */
.fc .fc-button.fc-button-active,
.fc .fc-button.fc-today-button.fc-button-active {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.25);
}

/* today単体で色ブレ防止 */
.fc .fc-button.fc-today-button {
  background-color: #d32f2f !important;
  border-color: #d32f2f !important;
  color: #ffffff !important;
}

/* 無効 */
.fc .fc-button:disabled {
  background-color: #ef9a9a !important;
  border-color: #ef9a9a !important;
  color: #ffffff !important;
  opacity: 1 !important;
  box-shadow: none;
}

/* 右側ボタンの寄せ（PC用） */
.fc .fc-toolbar-chunk:last-child {
  margin-right: 20px;
}

/* =================================
   shopping を“文字だけ”
   ================================= */
.fc .cat-shopping.fc-event,
.fc .cat-shopping .fc-event-main,
.fc .cat-shopping .fc-event-main-frame {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
}
.fc .fc-daygrid-event.cat-shopping {
  background: transparent !important;
  border: none !important;
}
.fc .cat-shopping .fc-event-title,
.fc .cat-shopping .fc-event-time {
  color: #b71c1c !important;
  font-weight: 700;
}

/* =================================
   スマホ最適化（ここが本体）
   ================================= */
@media (max-width: 768px) {

  /* タイトル小さく */
  .fc .fc-toolbar-title {
    font-size: 1.4em !important;
    margin: 8px !important;
    margin-top: 10px !important;
  }

  /* ヘッダーを折り返しても崩れない */
  .fc .fc-toolbar {
    flex-wrap: wrap !important;
    gap: 6px !important;
  }
  .fc .fc-toolbar-chunk {
    display: flex !important;
    align-items: center !important;
  }

  /* 右側ボタンを詰める */
  .fc .fc-toolbar-chunk:last-child {
    margin-right: 0 !important;
  }

  /* ボタンを小さく・タップしやすく */
  .fc .fc-button {
    padding: 0.35em 0.6em !important;
    font-size: 0.92em !important;
    border-radius: 10px !important;
  }

  /* 曜日・日付を少し小さく */
  .fc .fc-col-header-cell-cushion {
    font-size: 0.9em !important;
  }
  .fc .fc-daygrid-day-number {
    font-size: 0.9em !important;
    padding: 4px !important;
  }

  /* 予定の文字を小さく、行間を詰めて見切れにくく */
  .fc .fc-daygrid-event .fc-event-title {
    font-size: 0.85em !important;
    line-height: 1.15 !important;
  }

  /* カレンダー全体の上下余白を減らす */
  .fc .fc-view-harness {
    min-height: 72vh !important;
  }
}

/* さらに小さい端末（iPhone SEなど） */
@media (max-width: 420px) {
  .fc .fc-button {
    padding: 0.3em 0.5em !important;
    font-size: 0.86em !important;
  }
  .fc .fc-toolbar-title {
    font-size: 1.25em !important;
  }
}
"""

calendar(
    events=events,
    options=options,
    custom_css=custom_css,
    key="todo_calendar",
)
