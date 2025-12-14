import streamlit as st
from collections import defaultdict
from utils.ui import page_setup, task_list_view, reset_task_action_flags, apply_task_actions

page_setup()

st.header("📅 カレンダー（期限日ベース）")

tasks = [t for t in st.session_state.data["tasks"] if t.get("due_date")]

group = defaultdict(list)
for t in tasks:
    group[t["due_date"]].append(t)

reset_task_action_flags()

for due in sorted(group.keys()):
    st.subheader(due)
    task_list_view(group[due], show_category=True)

apply_task_actions()
