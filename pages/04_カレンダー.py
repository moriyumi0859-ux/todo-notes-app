import streamlit as st
import base64
from pathlib import Path
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

# 共通レイアウト（背景/カード/サイドバー等）
page_setup()

# カレンダーページだけ少し横幅を広く
st.markdown(
    """
    <style>
    section[data-testid="stMain"] .block-container{
        max-width: 1400px !important;   /* お好みで 1200〜1600 */
    }

    /* ===== 曜日ヘッダー（日=赤, 土=青） ===== */
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

    /* ===== 日付の数字も（日=赤, 土=青）に寄せる（一般的） ===== */
    .fc-daygrid-day.fc-day-sun .fc-daygrid-day-number { color: #e53935; }
    .fc-daygrid-day.fc-day-sat .fc-daygrid-day-number { color: #1e88e5; }

    /* ===== 今日をうっすら強調（一般的） ===== */
    .fc-daygrid-day.fc-day-today{
      background: rgba(255, 193, 7, 0.12) !important; /* うすい黄色 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header("📅 カレンダー（期限日ベース）")

# カレンダー周辺の装飾（白いカード）
def calendar_decorate():
    st.markdown(
        """
        <style>
        .calendar-wrap {
            position: relative;
            padding: 22px;
            margin-top: 12px;
            border-radius: 22px;
            background-color: rgba(255,255,255,0.88);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

calendar_decorate()
st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)

# -----------------------------
# tasks → events
# -----------------------------
tasks = st.session_state.get("data", {}).get("tasks", [])

events = []
for t in tasks:
    due = t.get("due_date")  # "YYYY-MM-DD"
    title = t.get("title")
    if due and title:
        # 完了なら✅を付ける（任意）
        prefix = "✅ " if t.get("done") else ""
        events.append({
            "title": prefix + title,
            "start": due,
            "allDay": True,
        })

# -----------------------------
# 祝日（日本の一般的な見え方：薄赤の背景）
# -----------------------------
today = dt.date.today()
year = today.year

for d, name in jpholiday.year_holidays(year):
    events.append({
        "title": name,  # 背景イベントなので通常は文字としては出ません（背景だけ）
        "start": d.isoformat(),
        "allDay": True,
        "display": "background",
        "backgroundColor": "rgba(229,57,53,0.10)",  # 薄赤
    })

options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,  # お好みで 800〜1000
}

calendar(events=events, options=options, key="todo_calendar")

st.markdown("</div>", unsafe_allow_html=True)
