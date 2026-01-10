import streamlit as st
from utils.ui import page_setup
from utils.models import Memo
from utils.storage import save_data

page_setup()

st.markdown(
    '<h2 style="font-size: 1.4rem; white-space: nowrap; margin-bottom: 1rem;">📝 フリーメモ</h2>', 
    unsafe_allow_html=True
)

with st.form("add_memo", clear_on_submit=True):
    text = st.text_area("メモを書く")
    submitted = st.form_submit_button("追加")

if submitted and text.strip():
    st.session_state.data["memos"].append(Memo.new(text).to_dict())
    save_data(st.session_state.data)
    st.toast("メモを追加しました ✅")

st.divider()

for m in reversed(st.session_state.data["memos"]):
    cols = st.columns([0.85, 0.15])
    with cols[0]:
        st.write(m["text"])
        st.caption(m.get("created_at", ""))
    with cols[1]:
        if st.button("削除", key=f"memo_{m['id']}"):
            st.session_state.data["memos"] = [
                x for x in st.session_state.data["memos"] if x["id"] != m["id"]
            ]
            save_data(st.session_state.data)
            st.rerun()
