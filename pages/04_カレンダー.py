import streamlit as st
import datetime as dt
import jpholiday
import base64
from pathlib import Path

from utils.ui import page_setup
from streamlit_calendar import calendar

# -----------------------------
# 0) 共通レイアウト
# -----------------------------
page_setup()
st.header("📅 カレンダー（期限日ベース）")

# -----------------------------
# 1) bg_calendar.png を確実に読み込む（存在チェック付き）
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]          # repo root
BG_PATH = ROOT / "assets" / "bg_calendar.png"

# デバッグ（必要な間だけONにしてください）
DEBUG = True
if DEBUG:
    st.caption(f"bg_calendar path: {BG_PATH}")
    st.caption(f"bg_calendar exists: {BG_PATH.exists()}")

if not BG_PATH.exists():
    st.error("assets/bg_calendar.png が見つかりません。GitHubにpushされているか確認してください。")
    st.stop()

bg_b64 = base64.b64encode(BG_PATH.read_bytes()).decode()

# -----------------------------
# 2) 見た目（一般的なカレンダー＋装飾PNG重ね）
#   - 日曜赤/土曜青、祝日薄赤、今日薄黄
#   - FullCalendar上部の白い横長バーを透明化
#   - 右上にbg_calendar.pngを重ねる（小さい別カレンダー等は出ない）
# -----------------------------
st.markdown(
    f"""
    <style>
    /* Streamlit上部の帯が気になる場合の保険 */
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
    }}
    [data-testid="stDecoration"] {{ display: none !important; }}

    /* このページだけ横幅広め */
    section[data-testid="stMain"] .block-container {{
        max-width: 1400px !important;
    }}

    /* カレンダーのカード（不透明な白） */
    .calendar-wrap {{
        position: relative;
        background: #ffffff !important;
        border-radius: 22px;
        padding: 20px 24px 24px 24px !important;
        margin-top: 10px !important;
        box-shadow: 0 14px 40px rgba(0,0,0,0.16);
        overflow: hidden;
    }}

    /* 右上に装飾PNGを“重ねる”（これがbg_calendar.pngの反映部分） */
    .calendar-wrap::after {{
        content: "";
        position: absolute;
        top: 10px;
        right: 10px;
        width: 240px;
        height: 240px;
        background-image: url("data:image/png;base64,{bg_b64}");
        background-size: contain;
        background-repeat: no-repeat;
        opacity: 0.95;
        pointer-events: none;
        z-index: 1;
    }}

    /* FullCalendar本体は装飾より上に表示 */
    .calendar-wrap .fc {{
        position: relative;
        z-index: 2;
    }}

    /* FullCalendar上部の白い横長バーを消す */
    .calendar-wrap .fc .fc-header-toolbar,
    .calendar-wrap .fc .fc-toolbar {{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0 !important;
    }}
    .calendar-wrap .fc .fc-header-toolbar {{
        margin-bottom: 10px !important;
    }}
    .calendar-wrap .fc .fc-toolbar-title {{
        padding-top: 6px !important;
    }}

    /* 日曜赤・土曜青（ヘッダー） */
    .fc-col-header-cell.fc-day-sun,
    .fc-col-header-cell.fc-day-sun a {{
        color: #e53935 !important;
        font-weight: 700;
    }}
    .fc-col-header-cell.fc-day-sat,
    .fc-col-header-cell.fc-day-sat a {{
        color: #1e88e5 !important;
        font-weight: 700;
    }}

    /* 日付の数字も色分け */
    .fc-daygrid-day.fc-day-sun .fc-daygrid-day-number {{ color: #e53935; }}
    .fc-daygrid-day.fc-day-sat .fc-daygrid-day-number {{ color: #1e88e5; }}

    /* 今日をうっすら強調 */
    .fc-daygrid-day.fc-day-today {{
        background: rgba(255, 193, 7, 0.12) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 3) tasks → events（期限日があるものだけ）
# -----------------------------
tasks = st.session_state.get("data", {}).get("tasks", [])
events = []

for t in tasks:
    due = t.get("due_date")   # "YYYY-MM-DD"
    title = t.get("title")
    if due and title:
        prefix = "✅ " if t.get("done") else ""
        events.append({"title": prefix + title, "start": due, "allDay": True})

# -----------------------------
# 4) 祝日（薄赤背景）
# -----------------------------
year = dt.date.today().year
for d, _name in jpholiday.year_holidays(year):
    events.append({
        "title": "holiday",
        "start": d.isoformat(),
        "allDay": True,
        "display": "background",
        "backgroundColor": "rgba(229,57,53,0.10)",
    })

# -----------------------------
# 5) カレンダー表示
# -----------------------------
options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 900,
    "headerToolbar": {"left": "title", "center": "", "right": "today prev,next"},
}

st.markdown('<div class="calendar-wrap">', unsafe_allow_html=True)
calendar(events=events, options=options, key="todo_calendar")
st.markdown("</div>", unsafe_allow_html=True)
