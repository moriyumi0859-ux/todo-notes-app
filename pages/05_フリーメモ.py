import streamlit as st

# --- 1. ログインチェック (必須) ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("ログインが必要です。ホーム画面からログインしてください。")
    st.stop()

# --- 2. インポート ---
from utils.ui import page_setup
from utils.models import Memo
from utils.storage import save_data

# ページ共通設定
page_setup()

# ヘッダー (スマホ対応)
st.markdown(
    '<h2 style="font-size: 1.4rem; white-space: nowrap; margin-bottom: 1rem;">📝 フリーメモ</h2>', 
    unsafe_allow_html=True
)

# --- 3. メモ追加フォーム ---
with st.form("add_memo", clear_on_submit=True):
    text = st.text_area("メモを書く")
    submitted = st.form_submit_button("追加")

if submitted and text.strip():
    # ログイン中のユーザーデータに追加
    st.session_state.data["memos"].append(Memo.new(text).to_dict())
    
    # 【重要】ユーザー名を指定して保存
    save_data(st.session_state.data, st.session_state.username)
    st.toast("メモを追加しました ✅")
    st.rerun()

st.divider()

# --- 4. メモ一覧表示と削除処理 ---
# 最新のメモが上にくるように逆順で表示
memos = st.session_state.data.get("memos", [])

for m in reversed(memos):
    cols = st.columns([0.85, 0.15])
    with cols[0]:
        st.write(m["text"])
        st.caption(m.get("created_at", ""))
    with cols[1]:
        # 削除ボタン
        if st.button("削除", key=f"memo_{m['id']}"):
            # 指定したID以外のメモを残す（＝削除）
            st.session_state.data["memos"] = [
                x for x in st.session_state.data["memos"] if x["id"] != m["id"]
            ]
            # 【重要】ユーザー名を指定して保存
            save_data(st.session_state.data, st.session_state.username)
            st.rerun()