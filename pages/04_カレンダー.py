import streamlit as st
import datetime as dt
import jpholiday

from utils.ui import page_setup
from streamlit_calendar import calendar

# =========================
# 0) 共通レイアウト
# =========================
page_setup()

st.toast("🧪 calendar page loaded: a8efc16", icon="✅")
st.write("commit:", "a8efc16")

st.header("📅 カレンダー（期限日ベース）")

# =========================
# 1) カレンダーページ専用CSS（白バー対策＋一般的な色）
# =========================
st.markdown(
    """
    <style>
    /* --- Streamlit上部の白いバー対策 --- */
    [data-testid="stHeader"],
    [data-testid="stToolbar"]{
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
    }
    [data-testid="stDecoration"]{ display:none !important; }

    /* 本文がヘッダーにめり込まないように */
    [data-testid="stMainBlockContainer"]{
        padding-top: 18px !important;
    }

    /* 外側カードは消して、カレンダーのカードだけを主役に */
    section[data-testid="stMain"] .block-container{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 0 24px 0 !important;
        margin-top: 0 !important;
        max-width: 1400px !important;
    }

    /* カレンダーの白カード（不透明） */
    .calendar-wrap{
        background: #fff !important;
        border-radius: 22px;
        padding: 20px 24px 24px 24px !important;
        margin-top: 10px !important;
        box-shadow: 0 14px 40px rgba(0,0,0,0.16);
    }

    /* ===== 一般的なカレンダー：日曜赤・土曜青 ===== */
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
# 2) tasks → events
# =========================
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

for t in tasks:
    due = t.get("due_date")
    title = t.get("title")
    if due and title:
        prefix = "✅ " if t.get("done") else ""
        events.append({"title": prefix + title, "start": due, "allDay": True})

# =========================
# 3) 祝日（薄赤背景）
# =========================
year = dt.date.today().year
for d, name in jpholiday.year_holidays(year):
    events.append({
        "title": name,
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
