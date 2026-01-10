import streamlit as st
from datetime import date, timedelta

# 1. ページ設定（必ず最初に行う）
st.set_page_config(page_title="To Do & Notes", layout="wide")

from utils.storage import save_data, load_data
from utils.constants import DEFAULT_BG_THEME
from utils.styles import apply_global_styles
from utils.theme import BG_MAP
from utils.ui import ensure_data_loaded, show_open_notifications
from utils.ui import task_list_view, reset_task_action_flags, apply_task_actions

# --- 🔑 ログイン・セッション管理 ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# 未ログイン時の表示
if not st.session_state.logged_in:
    st.title("🔐 To Do App ログイン")
    
    with st.form("login_form"):
        user_input = st.text_input("ユーザー名（英数字）")
        pw_input = st.text_input("パスワード", type="password")
        submit = st.form_submit_button("ログイン")
        
        if submit:
            # パスワードをここで自由に設定してください
            if user_input.strip() != "" and pw_input == "admin123":
                st.session_state.logged_in = True
                st.session_state.username = user_input
                # ログイン成功時にデータをロード（utils/storage.pyがユーザー名対応している前提）
                st.session_state.data = load_data(user_input)
                st.rerun()
            else:
                st.error("ユーザー名を入力するか、パスワードを確認してください")
    st.stop() # ログインするまでこれ以降のコードを実行しない

# --- 🏠 メイン画面（ログイン後） ---

# ログアウトボタンをサイドバーの一番上に配置
if st.sidebar.button("🚪 ログアウト"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.pop("data", None) # データをクリア
    st.rerun()

st.sidebar.caption(f"👤 ユーザー: {st.session_state.username}")

# ✅ data を必ず用意
ensure_data_loaded()

# settings 保険
st.session_state.data["settings"].setdefault("bg_theme", DEFAULT_BG_THEME)

# 背景テーマ選択（サイドバー）
st.sidebar.markdown("## 🎨 背景テーマ")
themes = list(BG_MAP.keys())

current = st.session_state.data["settings"]["bg_theme"]
idx = themes.index(current) if current in themes else 0
theme = st.sidebar.radio("背景を選ぶ", themes, index=idx)

if theme != current:
    st.session_state.data["settings"]["bg_theme"] = theme
    # ユーザー名を渡して保存
    save_data(st.session_state.data, st.session_state.username)
    st.toast("背景を変更しました ✅")

# ✅ 背景スタイル適用
apply_global_styles(st.session_state.data["settings"]["bg_theme"])

st.title("To Do & Notes")

# 起動時通知（1回だけ）
if "notified" not in st.session_state:
    show_open_notifications(st.session_state.data["tasks"])
    st.session_state.notified = True

st.info("👈️ 左のメニューから「プライベート / 仕事 / カレンダー」などを選んでください。")
st.success("✅️ 終わった予定にはチェックボックスにチェックを入れてください。")

st.subheader("📌 直近3日の予定")

today = date.today()
days = [
    ("今日", today),
    ("明日", today + timedelta(days=1)),
    ("明後日", today + timedelta(days=2)),
]

target_dates = {d.isoformat() for _, d in days}
upcoming = [t for t in st.session_state.data["tasks"] if t.get("due_date") in target_dates and (not t.get("done"))]

reset_task_action_flags()

if not upcoming:
    st.caption("直近3日の予定はまだありません。")
else:
    for label, day in days:
        iso = day.isoformat()
        day_tasks = [t for t in upcoming if t.get("due_date") == iso]
        if not day_tasks:
            continue

        st.markdown(f"### {label}（{iso}）")
        timed = [t for t in day_tasks if t.get("due_time")]
        untimed = [t for t in day_tasks if not t.get("due_time")]

        if timed:
            st.markdown("**🕘 時間あり**")
            task_list_view(timed, show_category=True)
        if untimed:
            st.markdown("**📌 時間なし（今日中）**")
            task_list_view(untimed, show_category=True)

apply_task_actions()

if st.button("💾 今すぐ保存"):
    save_data(st.session_state.data, st.session_state.username)
    st.toast("保存しました ✅")