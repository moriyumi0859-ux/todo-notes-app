import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

# =========================
# 0) 共通レイアウト（背景/カード/サイドバー等）
# =========================
page_setup()

st.header("📅 カレンダー（期限日ベース）")

# =========================
# 1) カレンダーページ専用CSS
#   - 余計な外側カード感を抑える
#   - カレンダーを不透明な白カードに
#   - 日曜赤/土曜青、祝日薄赤、今日薄黄
#   - FullCalendar上部の白い横長バー（toolbar背景）を消す
# =========================
st.markdown(
    """
    <style>
    /* --- Streamlit上部（白い帯が出る場合の保険）--- */
    [data-testid="stHeader"],
    [data-testid="stToolbar"]{
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
    }
    [data-testid="stDecoration"]{ display:none !important; }

    /* --- このページは少し横幅を広く --- */
    section[data-testid="stMain"] .block-container{
        max-width: 1400px !important;  /* 好みで 1200〜1600 */
    }

    /* --- カレンダーの白カード（不透明） --- */
    .calendar-wrap{
        background: #ffffff !important;
        border-radius: 22px;
        padding: 20px 24px 24px 24px !important;
        margin-top: 10px !important;
        box-shadow: 0 14px 40px rgba(0,0,0,0.16);
    }

    /* ===== FullCalendar上部の“白い横長バー”を消す ===== */
    .calendar-wrap .fc .fc-header-toolbar,
    .calendar-wrap .fc .fc-toolbar{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
    }
    .calendar-wrap .fc .fc-header-toolbar{
        margin-bottom: 10px !important;  /* 余白だけ残す */
    }
    .calendar-wrap .fc .fc-toolbar-title{
        padding-top: 6px !important;     /* タイトルが切れないように */
    }

    /* ===== 一般的な日本のカレンダー：日曜赤・土曜青 ===== */
    .fc-col-header-cell.fc-day-sun,
    .fc-col-header-cell.fc-day-sun a{
        color:#e53935 !important;
        font-weight:700;
    }
    .fc-col-header-cell.fc-day-sat,
    .fc-col-header-cell.fc-day-sat a{
        color:#1e88e5 !important;
        font-weight:700;
    }
    .fc-daygrid-day.fc-day-sun .fc-daygrid-day-number{ color:#e53935; }
    .fc-daygrid-day.fc-day-sat .fc-daygrid-day-number{ color:#1e88e5; }

    /* 今日をうっすら強調 */
    .fc-daygrid-day.fc-day-today{
        background: rgba(255,193,7,0.12) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 2) tasks → events（期限日があるタスクのみ）
# =========================
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

for t in tasks:
    due = t.get("due_date")   # "YYYY-MM-DD"
    title = t.get("title")
    if due and title:
        prefix = "✅ " if t.get("done") else ""
        events.append({"title": prefix + title, "start": due, "allDay": True})

# =========================
# 3) 祝日（薄赤の背景）
# =========================
year = dt.date.today().year
for d, _name in jpholiday.year_holidays(year):
    events.append({
        "title": "holiday",
        "start": d.isoformat(),
        "allDay": True,
        "display": "background",
        "backgroundColor": "rgba(229,57,53,0.10)",
    })

# =========================
# 4) カレンダー表示
# =========================
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

st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)
calendar(events=events, options=options, key="todo_calendar")
st.markdown('</div>', unsafe_allow_html=True)
