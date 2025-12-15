from __future__ import annotations
import streamlit as st

from utils.constants import (
    SURFACE_RGBA, APP_VEIL_RGBA, BLUR_PX, SIDEBAR_WIDTH_PX,
    RADIUS_PX, BORDER_RGBA, SHADOW_RGBA,
    CARD_PADDING_PX, CARD_MARGIN_PX, CARD_MARGIN_TOP_PX,
    MAIN_GAP_PX, MAIN_RIGHT_GAP_PX
)
from utils.theme import BG_MAP, img_to_base64


def apply_global_styles(bg_theme: str) -> None:
    path = BG_MAP.get(bg_theme)
    b64 = img_to_base64(path) if path else ""

    bg_css = ""
    if b64:
        bg_css = f"""
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        """

    st.markdown(
        f"""
<style>
{bg_css}

/* ===== 背景の上に敷く薄い幕 ===== */
[data-testid="stAppViewContainer"] {{
    background-color: {APP_VEIL_RGBA};
}}

/* ===== メイン領域の左右余白 ===== */
[data-testid="stMain"] {{
    padding-left: {MAIN_GAP_PX}px !important;
    padding-right: {MAIN_RIGHT_GAP_PX}px !important;
    background: transparent !important;
}}

/* ===== メイン：白い半透明カード（2段シャドウ） ===== */
.block-container {{
    background: {SURFACE_RGBA};
    border-radius: {RADIUS_PX}px;
    padding: {CARD_PADDING_PX}px;

    /* 🔽 ここが変更点（2段シャドウ） */
    box-shadow:
        0 12px 32px rgba(0, 0, 0, 0.18),
        0 4px 12px rgba(0, 0, 0, 0.10);

    backdrop-filter: blur({BLUR_PX}px);
    -webkit-backdrop-filter: blur({BLUR_PX}px);
    border: 1px solid {BORDER_RGBA};
    margin: {CARD_MARGIN_TOP_PX}px {CARD_MARGIN_PX}px {CARD_MARGIN_PX}px;
}}

/* ===== サイドバー ===== */
[data-testid="stSidebar"] {{
    width: {SIDEBAR_WIDTH_PX}px;
    min-width: {SIDEBAR_WIDTH_PX}px;
    max-width: {SIDEBAR_WIDTH_PX}px;
    background: {SURFACE_RGBA};
    backdrop-filter: blur({BLUR_PX}px);
    -webkit-backdrop-filter: blur({BLUR_PX}px);
    border-right: 1px solid {BORDER_RGBA};
    box-shadow: 10px 0 26px rgba(0,0,0,0.08);
}}

/* ===== タスク行（共通） ===== */
.task-row {{
    padding: 6px 8px;
    border-radius: 8px;
}}

/* プライベート（淡いグリーン） */
.task-private {{
    background-color: rgba(76, 175, 80, 0.15);
    border: 1px solid rgba(76, 175, 80, 0.22);
}}

/* 仕事（淡いブルー） */
.task-work {{
    background-color: rgba(33, 150, 243, 0.15);
    border: 1px solid rgba(33, 150, 243, 0.22);
}}

/* 買い物（フラット） */
.task-shopping {{
    background-color: transparent;
    border: none;
    color: #c62828;
}}

</style>
""",
        unsafe_allow_html=True,
    )
