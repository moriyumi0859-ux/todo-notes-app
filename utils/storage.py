import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from typing import Any, Dict, List
import uuid
from datetime import datetime
from utils.constants import DEFAULT_BG_THEME

# ==========================================
# ⚙️ 設定（ここを書き換えてください）
# ==========================================
SPREADSHEET_ID = "1QaBDNoCNOh6EKqGwnUli1OxTXmg7jI4jqfGzCasXrlM"

# ==========================================
# 🔑 スプレッドシート接続関数
# ==========================================
def get_gspread_client():
    """Streamlit Secretsを使用してGoogle Sheets APIに接続（決定版）"""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 【重要】 st.secrets をそのまま使わず、必ず標準の辞書型(dict)に変換する
    # これにより、ライブラリが「ファイル名」と勘違いするのを防ぎます
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # 秘密鍵の改行コード（\n）が文字列として入っている場合の対策
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    # from_service_account_info (辞書から読み込む) を使用
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(credentials)

def get_sheet(sheet_name: str):
    """特定のシートを取得"""
    client = get_gspread_client()
    sh = client.open_by_key(SPREADSHEET_ID)
    return sh.worksheet(sheet_name)

# ==========================================
# 💾 データ操作関数
# ==========================================

def load_data(username: str) -> Dict[str, Any]:
    """スプレッドシートからユーザー固有のデータを読み込む"""
    try:
        # 1. Tasksの読み込み
        task_sheet = get_sheet("tasks")
        all_tasks = task_sheet.get_all_records()
        user_tasks = [t for t in all_tasks if str(t.get("username")) == username]
        
        # 2. Memosの読み込み
        memo_sheet = get_sheet("memos")
        all_memos = memo_sheet.get_all_records()
        user_memos = [m for m in all_memos if str(m.get("username")) == username]

        # 3. Settings (Userテーマ) の読み込み
        user_sheet = get_sheet("users")
        all_users = user_sheet.get_all_records()
        user_info = next((u for u in all_users if str(u.get("username")) == username), None)
        
        bg_theme = user_info.get("bg_theme") if user_info else DEFAULT_BG_THEME
        if not bg_theme: bg_theme = DEFAULT_BG_THEME

        return {
            "tasks": user_tasks,
            "memos": user_memos,
            "settings": {"bg_theme": bg_theme}
        }
    except Exception as e:
        st.error(f"データ読み込みエラー: {e}")
        return {"tasks": [], "memos": [], "settings": {"bg_theme": DEFAULT_BG_THEME}}

def save_data(data: Dict[str, Any], username: str) -> None:
    """スプレッドシートのデータを更新（差分だけではなく全置換に近い処理）"""
    try:
        # 1. Tasksの保存 (一度そのユーザーの行を消して書き直すのは大変なので、
        #    全データ取得 → そのユーザー以外を保持 → 新しいデータを合体 → 全書き換え)
        task_sheet = get_sheet("tasks")
        all_tasks = task_sheet.get_all_records()
        other_users_tasks = [t for t in all_tasks if str(t.get("username")) != username]
        
        # 今回のユーザーデータを整形
        new_user_tasks = []
        for t in data["tasks"]:
            new_user_tasks.append([
                t.get("id"), username, t.get("category"), t.get("title"),
                t.get("due_date"), t.get("due_time"), str(t.get("done")).upper(), t.get("notes")
            ])
        
        # シートをクリアして見出しを書き込み、全データを再投入
        task_sheet.clear()
        task_sheet.append_row(["id", "username", "category", "title", "due_date", "due_time", "done", "notes"])
        
        # 他のユーザーのデータも整形して戻す
        others_formatted = [[row[k] for k in ["id", "username", "category", "title", "due_date", "due_time", "done", "notes"]] for row in other_users_tasks]
        
        if others_formatted:
            task_sheet.append_rows(others_formatted)
        if new_user_tasks:
            task_sheet.append_rows(new_user_tasks)

        # 2. Memosの保存 (同様のロジック)
        memo_sheet = get_sheet("memos")
        all_memos = memo_sheet.get_all_records()
        other_memos = [m for m in all_memos if str(m.get("username")) != username]
        
        new_user_memos = [[m.get("id"), username, m.get("text"), m.get("created_at")] for m in data["memos"]]
        
        memo_sheet.clear()
        memo_sheet.append_row(["id", "username", "text", "created_at"])
        others_memo_formatted = [[row[k] for k in ["id", "username", "text", "created_at"]] for row in other_memos]
        
        if others_memo_formatted:
            memo_sheet.append_rows(others_memo_formatted)
        if new_user_memos:
            memo_sheet.append_rows(new_user_memos)

        # 3. Settings (bg_theme) の保存
        user_sheet = get_sheet("users")
        all_users = user_sheet.get_all_records()
        
        # ユーザーがいれば更新、いなければ追加
        found = False
        for idx, u in enumerate(all_users):
            if str(u.get("username")) == username:
                user_sheet.update_cell(idx + 2, 3, data["settings"]["bg_theme"]) # 3列目がbg_theme
                found = True
                break
        if not found:
            user_sheet.append_row([username, "admin123", data["settings"]["bg_theme"]])

    except Exception as e:
        st.error(f"データ保存エラー: {e}")

def user_exists(username: str) -> bool:
    """ユーザーがusersシートに存在するか確認"""
    try:
        user_sheet = get_sheet("users")
        all_users = user_sheet.get_all_records()
        return any(str(u.get("username")) == username for u in all_users)
    except:
        return False

DEFAULT_DATA: Dict[str, Any] = {
    "tasks": [],
    "memos": [],
    "settings": {"bg_theme": DEFAULT_BG_THEME},
}

def verify_user(username, password) -> bool:
    """スプレッドシートの users シートからユーザー名とパスワードを照合する"""
    try:
        user_sheet = get_sheet("users")
        all_users = user_sheet.get_all_records()
        for u in all_users:
            # スプレッドシートの列名 username と password に一致するか確認
            if str(u.get("username")) == username and str(u.get("password")) == password:
                return True
        return False
    except Exception as e:
        print(f"Auth Error: {e}")
        return False