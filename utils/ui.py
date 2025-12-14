# utils/ui.py
from __future__ import annotations
import streamlit as st
from datetime import date
from typing import Any, Dict, List

from utils.storage import load_data, save_data
from utils.constants import DEFAULT_BG_THEME
from utils.styles import apply_global_styles


#✅ カテゴリ表示用ラベル

CATEGORY_LABEL = {
    "private": "プライベート",
    "work": "仕事",
    "shopping": "買い物",
}


def ensure_data_loaded() -> None:
    if "data" not in st.session_state:
        st.session_state.data = load_data()
    st.session_state.data.setdefault("tasks", [])
    st.session_state.data.setdefault("memos", [])
    st.session_state.data.setdefault("settings", {})


def page_setup() -> None:
    """全ページ共通：dataロード + settings保険 + 背景/カード/サイドバー適用"""
    ensure_data_loaded()
    st.session_state.data["settings"].setdefault("bg_theme", DEFAULT_BG_THEME)
    apply_global_styles(st.session_state.data["settings"]["bg_theme"])


def show_open_notifications(tasks: List[Dict[str, Any]]) -> None:
    today = date.today().isoformat()
    overdue = [t for t in tasks if (not t.get("done")) and t.get("due_date") and t["due_date"] < today]
    due_today = [t for t in tasks if (not t.get("done")) and t.get("due_date") == today]
    if overdue:
        st.error(f"⚠ 期限切れのタスクが {len(overdue)} 件あります")
    if due_today:
        st.warning(f"📅 今日が期限のタスクが {len(due_today)} 件あります")


def _sort_key(t: Dict[str, Any]):
    due_date = t.get("due_date") or "9999-12-31"
    due_time = t.get("due_time") or "99:99"  # 時間なしは後ろ
    return (t.get("done", False), due_date, due_time, t.get("created_at", ""))


def task_list_view(tasks: List[Dict[str, Any]], *, show_category: bool = False) -> None:
    tasks_sorted = sorted(tasks, key=_sort_key)

    for t in tasks_sorted:
        cols = st.columns([0.08, 0.62, 0.18, 0.12])

        with cols[0]:
            done = st.checkbox("", value=t.get("done", False), key=f"done_{t['id']}")

        with cols[1]:
            title = t.get("title", "")
            if show_category:
                cat = t.get("category", "")
                label = CATEGORY_LABEL.get(cat, cat)  # CATEGORY_LABEL がある前提
                title = f"[{label}] {title}"

            category = t.get("category")
            if category == "private":
                css_class = "task-row task-private"
            elif category == "work":
                css_class = "task-row task-work"
            elif category == "shopping":
                css_class = "task-row task-shopping"
            else:
                css_class = "task-row"

            st.markdown(
                f'<div class="{css_class}"><b>{title}</b></div>',
                unsafe_allow_html=True,
            )

            if t.get("notes"):
                st.caption(t["notes"])

        with cols[2]:
            d = t.get("due_date") or "—"
            tm = t.get("due_time")
            st.write(f"{d} {tm}" if tm else d)

        with cols[3]:
            if st.button("削除", key=f"del_{t['id']}"):
                st.session_state._delete_task_id = t["id"]

        if done != t.get("done", False):
            st.session_state._toggle_task_id = t["id"]
            st.session_state._toggle_task_value = done


def reset_task_action_flags() -> None:
    st.session_state.pop("_toggle_task_id", None)
    st.session_state.pop("_toggle_task_value", None)
    st.session_state.pop("_delete_task_id", None)


def apply_task_actions() -> None:
    tid = st.session_state.get("_toggle_task_id")
    if tid is not None:
        for t in st.session_state.data["tasks"]:
            if t["id"] == tid:
                t["done"] = st.session_state.get("_toggle_task_value", False)
                break
        save_data(st.session_state.data)
        st.rerun()

    did = st.session_state.get("_delete_task_id")
    if did is not None:
        st.session_state.data["tasks"] = [t for t in st.session_state.data["tasks"] if t["id"] != did]
        save_data(st.session_state.data)
        st.rerun()
