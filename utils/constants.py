# utils/constants.py

# 初期背景テーマ（BG_MAPのキーと一致させる）
DEFAULT_BG_THEME = "ボタニカル1"

# 透明度（メインカード＆サイドバーで統一）
SURFACE_RGBA = "rgba(255,255,255,0.82)"

# 背景の上に敷く薄い“全体幕”（カード導入後は薄め推奨）
APP_VEIL_RGBA = "rgba(255,255,255,0.05)"

# ぼかし
BLUR_PX = 6

# サイドバー幅
SIDEBAR_WIDTH_PX = 240

# 角丸・影・枠線
RADIUS_PX = 18
BORDER_RGBA = "rgba(255,255,255,0.35)"
SHADOW_RGBA = "rgba(0,0,0,0.12)"

# 余白
CARD_PADDING_PX = 22
CARD_MARGIN_PX = 16
CARD_MARGIN_TOP_PX = 100

# サイドバーとメインカードの間の余白
MAIN_GAP_PX = 12  # 8〜20 で好み調整
# 右（画面端側）※ 同じでOK
MAIN_RIGHT_GAP_PX = 12

PRIVATE_BG_RGBA = "rgba(76, 175, 80, 0.15)"   # グリーン
WORK_BG_RGBA    = "rgba(33, 150, 243, 0.15)"  # ブルー