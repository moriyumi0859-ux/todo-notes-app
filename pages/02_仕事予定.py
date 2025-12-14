import streamlit as st
import datetime

from utils.ui import page_setup, task_list_view, reset_task_action_flags, apply_task_actions
from utils.models import Task
from utils.storage import save_data

page_setup()

CATEGORY = "work"
st.header("💼 仕事予定")

with st.container():
    st.markdown("##### ⚙️ オプション")
    use_time = st.checkbox(
        "⏰ 時間を設定する",
        value=False,
        key="use_time_work",
    )

with st.form("add_work", clear_on_submit=True):
    title = st.text_input("予定 / タスク", placeholder="例：定例MTG、資料作成、提出など")
    due = st.date_input("日付（任意）", value=None)

    due_time_obj = st.time_input(
        "時間",
        value=datetime.time(9, 0),
        disabled=not st.session_state["use_time_work"],
        key="time_work",
    )

    notes = st.text_area("メモ（任意）", placeholder="例：場所、参加者、URL、目的など")
    submitted = st.form_submit_button("追加")

if submitted and title.strip():
    due_iso = due.isoformat() if due else None
    due_time = due_time_obj.strftime("%H:%M") if st.session_state["use_time_work"] else None

    task = Task.new(
        title=title,
        category=CATEGORY,
        due_date=due_iso,
        due_time=due_time,
        notes=notes,
    ).to_dict()

    st.session_state.data["tasks"].append(task)
    save_data(st.session_state.data)
    st.toast("追加しました ✅")

tasks = [t for t in st.session_state.data["tasks"] if t.get("category") == CATEGORY]
reset_task_action_flags()
task_list_view(tasks)
apply_task_actions()
