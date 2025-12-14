import streamlit as st
import datetime

from utils.ui import page_setup, task_list_view, reset_task_action_flags, apply_task_actions
from utils.models import Task
from utils.storage import save_data

page_setup()

CATEGORY = "private"
st.header("🏠 プライベート予定")

with st.container():
    st.markdown("##### ⚙️ オプション")
    use_time = st.checkbox(
        "⏰ 時間を設定する",
        value=False,
        key="use_time_private",
    )


with st.form("add_private", clear_on_submit=True):
    title = st.text_input("予定 / タスク", placeholder="例：病院の予約を入れる")
    due = st.date_input("日付（任意）", value=None)

    due_time_obj = st.time_input(
        "時間",
        value=datetime.time(9, 0),
        disabled=not st.session_state["use_time_private"],
        key="time_private",
    )

    notes = st.text_area("メモ（任意）")
    submitted = st.form_submit_button("追加")

if submitted and title.strip():
    due_iso = due.isoformat() if due else None
    due_time = due_time_obj.strftime("%H:%M") if st.session_state["use_time_private"] else None

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
