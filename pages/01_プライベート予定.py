import streamlit as st
import datetime

# --- 1. ログインチェック (必ず最初に入れる) ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("ログインが必要です。ホーム画面からログインしてください。")
    st.stop()

# --- 2. 必要なライブラリのインポート ---
from utils.ui import page_setup, task_list_view, reset_task_action_flags, apply_task_actions
from utils.models import Task
from utils.storage import save_data

# ページ共通設定（データロードなど）
page_setup()

CATEGORY = "private"

# --- 3. ヘッダー表示 (スマホ対応版) ---
st.markdown(
    '<h2 style="font-size: 1.4rem; white-space: nowrap; margin-bottom: 1rem;">🏠 プライベート予定</h2>', 
    unsafe_allow_html=True
)

# --- 4. オプション設定 ---
with st.container():
    st.markdown("##### ⚙️ オプション")
    use_time = st.checkbox(
        "⏰ 時間を設定する",
        value=False,
        key="use_time_private",
    )

# --- 5. タスク追加フォーム ---
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

# --- 6. 保存処理 (ユーザー名を追加) ---
if submitted and title.strip():
    due_iso = due.isoformat() if due else None
    due_time = due_time_obj.strftime("%H:%M") if st.session_state["use_time_private"] else None

    # Taskの作成
    task = Task.new(
        title=title,
        category=CATEGORY,
        due_date=due_iso,
        due_time=due_time,
        notes=notes,
    ).to_dict()

    # セッション内のデータに追加
    st.session_state.data["tasks"].append(task)
    
    # 【重要】現在のログインユーザー名を指定して保存
    save_data(st.session_state.data, st.session_state.username)
    
    st.toast("追加しました ✅")
    st.rerun() # リストを即座に更新

# --- 7. タスク一覧表示 ---
# ログイン中のユーザーのデータから、現在のカテゴリーのみ抽出
tasks = [t for t in st.session_state.data.get("tasks", []) if t.get("category") == CATEGORY]

reset_task_action_flags()
task_list_view(tasks)
apply_task_actions()