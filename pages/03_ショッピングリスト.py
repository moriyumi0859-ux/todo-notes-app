import streamlit as st
from datetime import date

# --- 1. ログインチェック (必須) ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("ログインが必要です。ホーム画面からログインしてください。")
    st.stop()

# --- 2. インポート ---
from utils.ui import page_setup
from utils.models import Task
from utils.storage import save_data

# ページ共通設定
page_setup()

CATEGORY = "shopping"

# --- 3. ヘッダー表示 (スマホ対応) ---
st.markdown(
    '<h2 style="font-size: 1.4rem; white-space: nowrap; margin-bottom: 1rem;">🛒 ショッピングリスト</h2>', 
    unsafe_allow_html=True
)

# --- 4. 追加フォーム ---
with st.form("add_shopping", clear_on_submit=True):
    due = st.date_input("買う日", value=date.today())
    title = st.text_input("買うもの", placeholder="例：牛乳、洗剤、電池")
    submitted = st.form_submit_button("追加")

if submitted and title.strip():
    task = Task.new(
        title=title,
        category=CATEGORY,
        due_date=due.isoformat(),
        due_time=None,
        notes="", 
    ).to_dict()

    st.session_state.data["tasks"].append(task)
    # 【修正】ユーザー名を指定して保存
    save_data(st.session_state.data, st.session_state.username)
    st.toast("追加しました ✅")
    st.rerun()

st.divider()

# --- 5. 一覧表示ロジック ---
shopping_tasks = [t for t in st.session_state.data.get("tasks", []) if t.get("category") == CATEGORY]

def _sort_key(t):
    return (t.get("done", False), t.get("due_date") or "9999-12-31", t.get("created_at", ""))

shopping_tasks = sorted(shopping_tasks, key=_sort_key)

# 操作フラグの初期化
if "_shopping_toggle_id" not in st.session_state:
    st.session_state._shopping_toggle_id = None
if "_shopping_delete_id" not in st.session_state:
    st.session_state._shopping_delete_id = None

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

# --- 6. 反映処理 (ここでもユーザー名を指定) ---
tid = st.session_state.get("_shopping_toggle_id")
if tid is not None:
    for x in st.session_state.data["tasks"]:
        if x.get("id") == tid:
            x["done"] = st.session_state.get("_shopping_toggle_value", False)
            break
    # 【修正】ユーザー名を指定して保存
    save_data(st.session_state.data, st.session_state.username)
    st.session_state._shopping_toggle_id = None # フラグを戻す
    st.rerun()

did = st.session_state.get("_shopping_delete_id")
if did is not None:
    st.session_state.data["tasks"] = [x for x in st.session_state.data["tasks"] if x.get("id") != did]
    # 【修正】ユーザー名を指定して保存
    save_data(st.session_state.data, st.session_state.username)
    st.session_state._shopping_delete_id = None # フラグを戻す
    st.rerun()