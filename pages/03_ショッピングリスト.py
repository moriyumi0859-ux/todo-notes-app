import streamlit as st
from datetime import date

from utils.ui import page_setup
from utils.models import Task
from utils.storage import save_data

page_setup()

CATEGORY = "shopping"
st.markdown(
    '<h2 style="font-size: 1.4rem; white-space: nowrap; margin-bottom: 1rem;">🛒 ショッピングリスト</h2>', 
    unsafe_allow_html=True
)

# --- 追加フォーム（チェックボックス無し / メモ無し） ---
with st.form("add_shopping", clear_on_submit=True):
    due = st.date_input("買う日", value=date.today())  # ✅ 常に有効＆安定
    title = st.text_input("買うもの", placeholder="例：牛乳、洗剤、電池")
    submitted = st.form_submit_button("追加")

if submitted and title.strip():
    task = Task.new(
        title=title,
        category=CATEGORY,
        due_date=due.isoformat(),  # ✅ 必ず入る（動かない問題が起きにくい）
        due_time=None,
        notes="",  # メモは使わないので空文字
    ).to_dict()

    st.session_state.data["tasks"].append(task)
    save_data(st.session_state.data)
    st.toast("追加しました ✅")

st.divider()

# --- 一覧（買う日 / 買うもの / チェック / 削除） ---
shopping_tasks = [t for t in st.session_state.data["tasks"] if t.get("category") == CATEGORY]

def _sort_key(t):
    return (t.get("done", False), t.get("due_date") or "9999-12-31", t.get("created_at", ""))

shopping_tasks = sorted(shopping_tasks, key=_sort_key)

# このページ専用の操作フラグ
st.session_state.pop("_shopping_toggle_id", None)
st.session_state.pop("_shopping_toggle_value", None)
st.session_state.pop("_shopping_delete_id", None)

if not shopping_tasks:
    st.caption("買うものはまだありません。")
else:
    for t in shopping_tasks:
        cols = st.columns([0.22, 0.60, 0.10, 0.08])

        with cols[0]:
            st.write(t.get("due_date") or "—")

        with cols[1]:
            st.write(f"**{t.get('title','')}**")

        with cols[2]:
            done = st.checkbox("", value=t.get("done", False), key=f"shop_done_{t['id']}")
            if done != t.get("done", False):
                st.session_state._shopping_toggle_id = t["id"]
                st.session_state._shopping_toggle_value = done

        with cols[3]:
            if st.button("削除", key=f"shop_del_{t['id']}"):
                st.session_state._shopping_delete_id = t["id"]

# --- 反映処理 ---
tid = st.session_state.get("_shopping_toggle_id")
if tid is not None:
    for x in st.session_state.data["tasks"]:
        if x.get("id") == tid:
            x["done"] = st.session_state.get("_shopping_toggle_value", False)
            break
    save_data(st.session_state.data)
    st.rerun()

did = st.session_state.get("_shopping_delete_id")
if did is not None:
    st.session_state.data["tasks"] = [x for x in st.session_state.data["tasks"] if x.get("id") != did]
    save_data(st.session_state.data)
    st.rerun()
