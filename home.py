import streamlit as st
from datetime import date, timedelta

# 1. ページ設定（必ず最初に行う）
st.set_page_config(page_title="To Do & Notes", layout="wide")

from utils.storage import save_data, load_data, user_exists, DEFAULT_DATA
from utils.constants import DEFAULT_BG_THEME
from utils.styles import apply_global_styles
from utils.theme import BG_MAP
from utils.ui import ensure_data_loaded, show_open_notifications
from utils.ui import task_list_view, reset_task_action_flags, apply_task_actions

# --- 🔑 ログイン・セッション管理 ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- 🔒 ログインしていない時の処理 ---
if not st.session_state.logged_in:
    # サイドバー（メニュー）を非表示にする
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.title("🔐 To Do App")
    
    # ログインと新規登録の切り替え
    tab_login, tab_signup = st.tabs(["ログイン", "新規登録"])

    with tab_login:
        with st.form("login_form"):
            user_input = st.text_input("ユーザー名")
            pw_input = st.text_input("パスワード", type="password")
            submit = st.form_submit_button("ログイン")
            
            if submit:
                # ユーザーが存在し、パスワードが合致するか（現状は admin123 固定）
                if user_input.strip() != "" and pw_input == "admin123":
                    if user_exists(user_input):
                        st.session_state.logged_in = True
                        st.session_state.username = user_input
                        st.session_state.data = load_data(user_input)
                        st.rerun()
                    else:
                        st.error("そのユーザー名は登録されていません")
                else:
                    st.error("ユーザー名を入力するか、パスワードを確認してください")

    with tab_signup:
        with st.form("signup_form"):
            new_user = st.text_input("希望するユーザー名（英数字のみ）")
            new_pw = st.text_input("設定するパスワード（現在は admin123 のみ有効）", type="password")
            signup_submit = st.form_submit_button("新規登録")
            
            if signup_submit:
                if not new_user.strip():
                    st.error("ユーザー名を入力してください")
                elif user_exists(new_user):
                    st.error("このユーザー名は既に使われています")
                elif new_pw != "admin123":
                    st.error("現在は共通パスワード admin123 のみ登録可能です")
                else:
                    # 新規ユーザー用のデータファイルを作成
                    save_data(DEFAULT_DATA, new_user)
                    st.success("✅ 登録が完了しました！ログインタブからログインしてください")

    st.stop() # ログインするまで下のメイン画面は読み込まない

# --- 🏠 メイン画面（ログイン後のみ表示） ---

# ログアウトボタン
if st.sidebar.button("🚪 ログアウト"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.pop("data", None)
    st.rerun()

st.sidebar.caption(f"👤 ユーザー: {st.session_state.username}")

# ✅ data を必ず用意
ensure_data_loaded()

# settings 保険
st.session_state.data["settings"].setdefault("bg_theme", DEFAULT_BG_THEME)

# 背景テーマ選択
st.sidebar.markdown("## 🎨 背景テーマ")
themes = list(BG_MAP.keys())
current = st.session_state.data["settings"]["bg_theme"]
idx = themes.index(current) if current in themes else 0
theme = st.sidebar.radio("背景を選ぶ", themes, index=idx)

if theme != current:
    st.session_state.data["settings"]["bg_theme"] = theme
    save_data(st.session_state.data, st.session_state.username)
    st.toast("背景を変更しました ✅")

# 背景スタイル適用
apply_global_styles(st.session_state.data["settings"]["bg_theme"])

st.title("To Do & Notes")

# 起動時通知
if "notified" not in st.session_state:
    show_open_notifications(st.session_state.data["tasks"])
    st.session_state.notified = True

st.info("👈️ 左のメニューから予定を選んでください。")

st.subheader("📌 直近3日の予定")

today = date.today()
days = [("今日", today), ("明日", today + timedelta(days=1)), ("明後日", today + timedelta(days=2))]
target_dates = {d.isoformat() for _, d in days}
upcoming = [t for t in st.session_state.data["tasks"] if t.get("due_date") in target_dates and (not t.get("done"))]

reset_task_action_flags()

if not upcoming:
    st.caption("直近3日の予定はまだありません。")
else:
    for label, day in days:
        iso = day.isoformat()
        day_tasks = [t for t in upcoming if t.get("due_date") == iso]
        if not day_tasks: continue
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