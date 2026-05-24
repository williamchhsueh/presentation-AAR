#!/usr/bin/env python3
"""
build_appendix.py — 從 appendix.md 生成 AAR 技術附錄（34 張）。

內容來源：appendix.md（A1–A26，6 大主題）
視覺權威：vis_style.md（沿用主 deck token / 元件 / helpers）
輸出：ppt/AAR_Appendix_v1.pptx（13.333" x 7.5"）
執行：poetry run python code/build_appendix.py

結構（34 張）：
  Cover(1) + Divider A + A1–A5      = 7
  Divider B + B1–B4                  = 5
  Divider C + C1–C5                  = 6
  Divider D + D1–D4                  = 5
  Divider E + E1–E3                  = 4
  Divider F + F1–F5                  = 6
  Closing(1)                         = 1
"""

import os

from pptx.util import Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# 從 build_deck 載入色票、字級、helpers，重用 vis_style 元件
from build_deck import (
    prs, BLANK, BASE_DIR, FIG_DIR,
    BG_BASE, BG_DOSSIER, BG_PURE, PANEL, PANEL_2, PANEL_BAD, PANEL_GOOD,
    STROKE, STROKE_HUD, DIVIDER, TEXT_PRIM, TEXT_SEC, TEXT_MUTED, TEXT_ON_ACC,
    ACC_GOOD, ACC_GOOD_GLOW, ACC_WARN, ACC_BAD, ACC_BAD_DIM, ACC_DATA_BLUE,
    ROLE_PM, ROLE_DS, ROLE_SWE, ROLE_NOTE, ROLE_REF,
    LATIN, CJK, MONO,
    T_MEGA, T_MEGA_SM, T_QUOTE, T_H1, T_H2, T_BODY, T_BODY_SM, T_CAPTION,
    T_BADGE, T_STRIP,
    add_slide, set_notes, text, text_lines, rect, hline,
    tick_corners, panel, card, badge_role, status_dot,
    dossier_frame, mega_number, fig_embed, h1, quote_slide,
)

OUT = os.path.join(BASE_DIR, "ppt", "AAR_Appendix_v1.pptx")
TOTAL = 34  # cover + 6 dividers + 26 content + closing

# ── Appendix-specific helpers ──────────────────────────────────────────
APPENDIX_COPYRIGHT = "AAR Technical Appendix · Companion to AAR_Paper_Sharing_v4.1"


def ax_footer(slide, code=None):
    """附錄頁腳：右下顯示 'APPENDIX · A{n}'，左下沿用版權。"""
    text(slide, APPENDIX_COPYRIGHT, 4, 94.6, 62, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    if code is not None:
        text(slide, f"APPENDIX · {code}", 70, 94.6, 26, 4,
             size=T_CAPTION, color=TEXT_MUTED, align=PP_ALIGN.RIGHT, font='mono')


def ax_header(slide, theme_label):
    """附錄頁眉：頂部 'APPENDIX // THEME X — ...' 條帶。"""
    hline(slide, 4, 3.5, 92, color=STROKE_HUD, weight_pt=1.0)
    text(slide, f"APPENDIX // {theme_label}", 4, 4.2, 92, 3,
         size=T_STRIP, color=TEXT_MUTED, font='mono')


def ax_meta(slide, paper_ref, deck_tie=None):
    """每張內容頁右上小字：論文出處 + 主 deck 關聯。"""
    line = f"PAPER: {paper_ref}"
    if deck_tie:
        line += f"   //   MAIN DECK: {deck_tie}"
    text(slide, line, 4, 4.2, 92, 3,
         size=T_STRIP, color=TEXT_MUTED, font='mono', align=PP_ALIGN.RIGHT)


# ════════════════════════════════════════════════════════════════════════
# COVER + DIVIDERS
# ════════════════════════════════════════════════════════════════════════
def cover():
    sl = add_slide(BG_DOSSIER)
    dossier_frame(sl, "TECHNICAL APPENDIX",
                  "STATUS: REFERENCE // AUDIENCE: DATA SCIENCE",
                  "VERSION: v1 // DATE: 2026-05-23")
    text(sl, "AAR 簡報", 6, 22, 88, 11,
         size=T_MEGA_SM, bold=True, color=TEXT_PRIM)
    text(sl, "技術附錄", 6, 34, 88, 13,
         size=T_MEGA, bold=True, color=ACC_GOOD_GLOW)
    text(sl, "26 張 · 6 大主題 · 補上主 deck 為節奏所捨棄的實驗細節、方法內部、reward hacking 偵測機制、作者自陳限制。",
         6, 50, 88, 8, size=T_H2 - 2, color=TEXT_SEC, line_spacing=1.4)
    text(sl, "配套主簡報　·　AAR_Paper_Sharing_v4.1.pptx（31 張）",
         6, 62, 88, 5, size=T_BODY, color=TEXT_MUTED, font='mono')
    text(sl, "論文來源　　·　alignment.anthropic.com/2026/automated-w2s-researcher · Sec 1–7",
         6, 67, 88, 5, size=T_BODY, color=TEXT_MUTED, font='mono')

    themes = [("A", "實驗環境", "A1–A5"),
              ("B", "Scaffold 架構", "B1–B4"),
              ("C", "5 個方法", "C1–C5"),
              ("D", "Reward Hacking", "D1–D4"),
              ("E", "泛化與遷移", "E1–E3"),
              ("F", "討論與限制", "F1–F5")]
    cw, x = 14.5, 6.5
    for letter, name, span in themes:
        ix, iy, iw, ih = panel(sl, x, 76, cw, 14, stripe=ACC_GOOD)
        text(sl, letter, ix, iy, iw, 5,
             size=22, bold=True, color=ACC_GOOD, align=PP_ALIGN.CENTER, font='mono')
        text(sl, name, ix, iy + 5, iw, 4,
             size=T_BODY_SM, bold=True, color=TEXT_PRIM, align=PP_ALIGN.CENTER)
        text(sl, span, ix, iy + 8.5, iw, 3,
             size=T_CAPTION, color=TEXT_MUTED, align=PP_ALIGN.CENTER, font='mono')
        x += cw + 1.0
    set_notes(sl, """【封面｜技術附錄 v1】

用途：散會後留給 DS 同事的技術補充；或 Q&A 時根據問題類型快速調出對應主題。

26 張內容投影片 + 1 張封面 + 6 張主題分隔 + 1 張結語 = 共 34 張。

不採用主 deck 的「巨人」敘事框架；全文直接引用論文章節、數字、原句。""")


def _divider(letter, theme_zh, theme_en, subtitle, slide_list, note):
    sl = add_slide(BG_BASE)
    ax_header(sl, f"THEME {letter} — {theme_en.upper()}")
    text(sl, letter, 6, 16, 18, 22,
         size=T_MEGA, bold=True, color=ACC_GOOD_GLOW, font='mono',
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
    text(sl, f"主題 {letter}", 26, 20, 70, 7,
         size=T_H2, color=TEXT_MUTED, font='mono')
    text(sl, theme_zh, 26, 26, 70, 12,
         size=52, bold=True, color=TEXT_PRIM)
    text(sl, subtitle, 26, 40, 70, 6,
         size=T_BODY, italic=True, color=TEXT_SEC, line_spacing=1.4)
    n = len(slide_list)
    if n == 5:
        sy, sh, gap = 49.0, 7.5, 1.0
    elif n == 4:
        sy, sh, gap = 54.0, 8.0, 2.0
    else:
        sy, sh, gap = 56.0, 8.0, 2.0
    for code, title in slide_list:
        ix, iy, iw, ih = panel(sl, 6, sy, 90, sh, stripe=ACC_DATA_BLUE)
        text(sl, code, ix, iy, 8, ih,
             size=T_H2 - 2, bold=True, color=ACC_GOOD,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, font='mono')
        text(sl, title, ix + 9, iy, iw - 9, ih,
             size=T_BODY + 1, color=TEXT_PRIM,
             anchor=MSO_ANCHOR.MIDDLE)
        sy += sh + gap
    ax_footer(sl, f"{letter}·DIV")
    set_notes(sl, note)


def divider_A():
    _divider("A", "實驗環境", "Experimental Setup",
             "Models · Testbeds · Splits · Baselines · Eval API",
             [("A1", "Qwen1.5-0.5B-Chat (weak) × Qwen3-4B-Base (strong)"),
              ("A2", "三個 testbed + 抗 hack 設計"),
              ("A3", "Train/Test 分割架構（4 split × 3 testbed）"),
              ("A4", "兩位人類 7 天的具體內容（Baseline = 0.23）"),
              ("A5", "Evaluation API 與 unlimited submissions 的設計選擇")],
             "【分隔頁 A｜實驗環境】涵蓋 5 張投影片，建立後續所有討論的事實基礎。")


def divider_B():
    _divider("B", "Scaffold 架構", "Scaffold Architecture",
             "Dashboard · Forum · Storage · MCP tools · Autonomous vs Prescriptive · Directed vs Undirected",
             [("B1", "Dashboard / Forum / External Storage 三層架構"),
              ("B2", "AAR 可用的 3 個 MCP 工具"),
              ("B3", "Autonomous vs Prescriptive Scaffolding"),
              ("B4", "Directed vs Undirected（+ 第三種失敗）")],
             "【分隔頁 B｜Scaffold 架構】解釋為何 autonomous + directed 是論文最終的設計選擇。")


def divider_C():
    _divider("C", "AAR 發現的 5 個方法", "Five Methods Discovered",
             "11 family 分類法 · CCS+ES · EM Posterior · Overlap Density · MDL + Epiplexity",
             [("C1", "11 個 method family + Shannon entropy 量測"),
              ("C2", "CCS + Evolution Strategy Refinement（PGR=0.93，最高分）"),
              ("C3", "EM Posterior（PGR=0.78，後續被選去做 production transfer）"),
              ("C4", "Overlap Density（PGR=0.75，論文標為 'alien'）"),
              ("C5", "MDL Curriculum (0.68) + Epiplexity (0.62)")],
             "【分隔頁 C｜5 個方法】主 deck 完全略過 Sec 4 的方法細節；本主題補齊。")


def divider_D():
    _divider("D", "Reward Hacking 深探", "Reward Hacking Deep-Dive",
             "Dataset shortcuts · Seed cherry-picking · Label exfiltration · Unit test bypass",
             [("D1", "Hack 1: Dataset Shortcuts"),
              ("D2", "Hack 2: Seed Cherry-Picking via Unlimited Submissions"),
              ("D3", "Hack 3: Test Label Exfiltration"),
              ("D4", "Hack 4: Unit Test Bypass + Meta-Finding")],
             "【分隔頁 D｜Reward Hacking】主 deck Slide 21 只列名稱；本主題深入機制 + 作者自陳。")


def divider_E():
    _divider("E", "泛化、遷移、複雜度", "Generalization · Transfer · Complexity",
             "Cross-dataset transfer · Production scale failure · Complexity tracking",
             [("E1", "Cross-dataset transfer：兩個方法在 Code 上的不同命運"),
              ("E2", "Production scale transfer failure：EM Posterior → Sonnet 4.0"),
              ("E3", "Idea complexity tracking：3 個指標、後期持平")],
             "【分隔頁 E｜泛化】E2 是主 deck 完全沒提的失敗案例，DS 應特別關注。")


def divider_F():
    _divider("F", "討論、限制、未來工作", "Discussion · Limitations · Future Work",
             "LM self-evo vs heuristic ES · Finding sharing 3 variants · Generalization 3 scales · Alien science · Caveats",
             [("F1", "LM Self-evolution vs Heuristic Evolutionary Search"),
              ("F2", "Finding Sharing 3 個變體：local agentic search 勝出"),
              ("F3", "泛化的 3 種尺度限制 + OOD test 的盲點"),
              ("F4", "Richer logs of science、Alien science 與 legibility training"),
              ("F5", "論文未明說的 caveats（整理者觀察，非論文原文）")],
             "【分隔頁 F｜討論】F5 是整理者觀察，非論文內容；引用時務必標明。")


# ════════════════════════════════════════════════════════════════════════
# THEME A — Experimental Setup (A1–A5)
# ════════════════════════════════════════════════════════════════════════
def slide_A1():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 1 Models", deck_tie="—")
    h1(sl, "A1 · Models：Qwen1.5-0.5B-Chat (weak) × Qwen3-4B-Base (strong)",
       y=7.5, h=10, size=26)

    ix, iy, iw, ih = panel(sl, 4, 22, 44, 30, stripe=ACC_DATA_BLUE)
    text(sl, "WEAK SUPERVISOR", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "Qwen1.5-0.5B-Chat", ix, iy + 4, iw, 7,
         size=T_H2 + 2, bold=True, color=TEXT_PRIM)
    text(sl, "提供有噪聲、不完美的標籤", ix, iy + 12, iw, 5,
         size=T_BODY_SM, color=TEXT_SEC)
    text(sl, "→", 49, 32, 4, 10,
         size=36, color=ACC_GOOD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    ix, iy, iw, ih = panel(sl, 53, 22, 44, 30, stripe=ACC_GOOD)
    text(sl, "STRONG STUDENT", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "Qwen3-4B-Base", ix, iy + 4, iw, 7,
         size=T_H2 + 2, bold=True, color=TEXT_PRIM)
    text(sl, "以噪聲標籤做 fine-tuning；目標是逼近 ground-truth 天花板",
         ix, iy + 12, iw, 8, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)

    card(sl, 4, 56, 92, 26, title="選擇這對模型的 3 個條件（\"sweet spot\"）",
         body=[
             ("1.  弱模型與強模型之間有 substantial performance gap",
              {'size': T_BODY, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
             ("2.  弱模型在 testbeds 上 better-than-random（不是亂猜）",
              {'size': T_BODY, 'color': TEXT_PRIM, 'space_before': 4, 'line_spacing': 1.4}),
             ("3.  兩個模型都夠小 → 每次 fine-tuning run 不到 2 小時，可快速實驗",
              {'size': T_BODY, 'color': TEXT_PRIM, 'space_before': 4, 'line_spacing': 1.4}),
         ], stripe=ACC_WARN)

    badge_role(sl, 4, 86, 'NOTE')
    text(sl, "AAR 引擎本身是 Claude Opus 4.6（主 deck Slide 11 提及），與被研究的小模型是兩件事。",
         13, 86.1, 84, 5, size=T_BODY_SM, color=TEXT_SEC, italic=True)

    ax_footer(sl, "A1")
    set_notes(sl, """【A1｜Models】論文 Sec 1 Models。

核心：
- Weak supervisor：Qwen1.5-0.5B-Chat
- Strong student：Qwen3-4B-Base
- 三個條件：performance gap / better-than-random / 夠小（<2hr per fine-tune）

注意：AAR 引擎是 Claude Opus 4.6，與被研究的小模型不同層次。""")


def slide_A2():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 1 Datasets", deck_tie="—")
    h1(sl, "A2 · 三個 testbed + 抗 hack 設計", y=7.5, h=10, size=28)

    text(sl, "三個 binary classification testbed · 共同性質：不可用記憶 pre-training 資料解 ⋅ 多數 baseline 只能拿 PGR ≈ 0.2",
         4, 20, 92, 5, size=T_BODY, color=ACC_WARN, italic=True, line_spacing=1.3)

    testbeds = [("Chat Preference",
                 "RLHF preference pairs；hill-climbing 主戰場",
                 "OOD 來自 RMBench / RewardBench 2"),
                ("Math Verification",
                 "判斷數學解是否正確（binary）",
                 "保留給跨 dataset 泛化測試"),
                ("Coding Verification",
                 "判斷程式解是否通過 unit test（binary）",
                 "True/False 標籤在每個難度級別都平衡，防止用難度反推標籤")]
    sy, sh, gap = 26.0, 14.0, 2.0
    for name, role, anti_hack in testbeds:
        ix, iy, iw, ih = panel(sl, 4, sy, 92, sh, stripe=ACC_DATA_BLUE)
        text(sl, name, ix, iy, 28, ih,
             size=T_H2 - 2, bold=True, color=TEXT_PRIM, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, role, ix + 28, iy + 1.5, 36, ih,
             size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)
        text(sl, anti_hack, ix + 65, iy + 1.5, iw - 65, ih,
             size=T_BODY_SM, color=ACC_WARN, line_spacing=1.3, italic=True)
        sy += sh + gap

    card(sl, 4, 74, 92, 20, title="關鍵設計決策 + 引用原句",
         body=[
             ("hill-climbing 只用 Chat Preference；Math 與 Coding 保留給「跨 dataset 泛化測試」。",
              {'size': T_BODY_SM, 'color': TEXT_PRIM}),
             ('"We reserve math and coding only for evaluating idea generalization across datasets, '
              'because our AAR finds diverse ways to solve these two tasks without leveraging '
              'weak supervision or strong model latent capabilities at all."',
              {'size': T_BODY_SM - 1, 'color': TEXT_SEC, 'italic': True,
               'space_before': 3, 'line_spacing': 1.3}),
         ], stripe=ACC_WARN, title_size=T_BODY + 1)

    ax_footer(sl, "A2")
    set_notes(sl, """【A2｜三個 testbed + 抗 hack】論文 Sec 1 Datasets。

- 三個 binary classification testbed
- 多數 baseline 在這三個 testbed 上只能拿到 PGR ≈ 0.2
- 抗 hack 設計：不可記憶 pre-training data；coding 標籤難度平衡

關鍵設計：只用 Chat Preference 跑 hill-climbing；Math/Coding 是泛化測試。""")


def slide_A3():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 1 Datasets 表格", deck_tie="—")
    h1(sl, "A3 · Train/Test 分割架構（4 split × 3 testbed）", y=7.5, h=10, size=26)

    text(sl, "每個 testbed 有 4 個 split：weak teacher train / strong student train / ID test / OOD test。",
         4, 20, 92, 6, size=T_BODY, color=TEXT_SEC, italic=True, line_spacing=1.3)

    # Table header
    header_y = 30
    cols = [("Testbed", 4, 22),
            ("Train / ID Test", 26, 36),
            ("OOD Test", 62, 34)]
    rect(sl, 4, header_y, 92, 6.5, fill=PANEL_2, line_color=STROKE)
    for label, x, w in cols:
        text(sl, label, x + 0.5, header_y + 1, w - 1, 4.5,
             size=T_BODY_SM, bold=True, color=ACC_GOOD,
             anchor=MSO_ANCHOR.MIDDLE, font='mono')

    rows = [("Chat Preference", "HelpSteer2 · HelpSteer3", "RMBench · RewardBench 2"),
            ("Math Verification", "DAPO-Math-17K 的 queries", "AIME 2024 / 2025 的 queries"),
            ("Coding Verification", "TACO Easy / Medium 難度", "TACO Medium-hard / Very-hard")]
    ry = header_y + 6.5
    for testbed, train, ood in rows:
        rh = 8.5
        rect(sl, 4, ry, 92, rh, fill=PANEL, line_color=STROKE)
        text(sl, testbed, 4.5, ry + 1.5, 21, rh - 2,
             size=T_BODY_SM, bold=True, color=TEXT_PRIM, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, train, 26.5, ry + 1.5, 35, rh - 2,
             size=T_BODY_SM, color=TEXT_SEC, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, ood, 62.5, ry + 1.5, 33, rh - 2,
             size=T_BODY_SM, color=TEXT_SEC, anchor=MSO_ANCHOR.MIDDLE)
        ry += rh

    card(sl, 4, 82, 92, 8, title=None, stripe=ACC_WARN,
         body=[("⚠  OOD test 是論文「驗證泛化」的主要工具，但 Sec 7 警告 OOD test 抓不出 data/model-specific tricks（見 F3）。",
                {'size': T_BODY_SM, 'color': ACC_WARN, 'line_spacing': 1.3})])

    ax_footer(sl, "A3")
    set_notes(sl, """【A3｜Splits】論文 Sec 1 Datasets 表格直接重繪。

每 testbed 4 split：weak teacher train / strong student train / ID test / OOD test。
OOD test 用來驗證泛化，但 Sec 7 警告它抓不出 data/model-specific tricks。""")


def slide_A4():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 1 Baselines", deck_tie="深化 Slide 01 / 18")
    h1(sl, "A4 · 兩位人類 7 天的具體內容（Baseline = 0.23）", y=7.5, h=10, size=26)

    text(sl, "兩位 Anthropic 作者 × 7 天 × 4+1 個 baseline 方法。",
         4, 20, 92, 5, size=T_BODY, color=TEXT_SEC, italic=True)

    methods = [
        ("1", "Training on weak labels", "直接用 weak supervisor 的標籤訓練"),
        ("2", "Training on confident weak labels", "先濾掉信心低的標籤再訓練"),
        ("3", "Unsupervised elicitation", "zero-shot-based"),
        ("4", "Critic training", "RL the strong student：由 strong student 產生 critique 來協助 weak teacher"),
        ("+", "Zero-shot prompting", "用 Anthropic 內部已調得高度優化、用於 pre-trained base models 的 prompt"),
    ]
    sy, sh, gap = 26.0, 13.0, 0.5   # 26+5×13+4×0.5=93%; ih visual from iy=9.574%
    for num, name, desc in methods:
        is_extra = (num == "+")
        ix, iy, iw, ih = panel(sl, 4, sy, 56, sh,
                               stripe=(ACC_WARN if is_extra else ACC_DATA_BLUE))
        text(sl, num, ix, iy, 5, ih,
             size=22, bold=True, color=(ACC_WARN if is_extra else ACC_GOOD),
             font='mono', align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, name, ix + 6, iy + 0.3, iw - 6, 4.5,
             size=T_BODY, bold=True, color=TEXT_PRIM)
        text(sl, desc, ix + 6, iy + 5.0, iw - 6, 4.4,
             size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.2)
        sy += sh + gap

    ix, iy, iw, ih = panel(sl, 63, 26, 33, 67, stripe=ACC_GOOD, fill=PANEL_GOOD)
    text(sl, "BEST RESULT", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono', align=PP_ALIGN.CENTER)
    text(sl, "PGR", ix, iy + 7, iw, 8,
         size=T_H2, color=TEXT_SEC, align=PP_ALIGN.CENTER)
    text(sl, "0.23", ix, iy + 14, iw, 22,
         size=T_MEGA_SM, bold=True, color=ACC_GOOD_GLOW, align=PP_ALIGN.CENTER)
    text(sl, "Chat Preference (ID + OOD)", ix, iy + 38, iw, 5,
         size=T_BODY_SM, color=TEXT_SEC, align=PP_ALIGN.CENTER, italic=True)
    text(sl, "2 humans × 7 days",
         ix, iy + 44, iw, 5, size=T_BODY_SM, color=TEXT_MUTED,
         align=PP_ALIGN.CENTER, font='mono')

    ax_footer(sl, "A4")
    set_notes(sl, """【A4｜兩位人類 7 天】論文 Sec 1 Baselines。深化主 deck Slide 01 / 18 的 0.23 數字。

4 個從先前論文 adopt 的 baseline + 1 個 zero-shot prompting baseline。
最佳 PGR 0.23（Chat Preference，含 ID + OOD test data）。""")


def slide_A5():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 1 Evaluation", deck_tie="深化 Slide 21（reward hacking 根因）")
    h1(sl, "A5 · Evaluation API 與 unlimited submissions 的設計選擇",
       y=7.5, h=10, size=24)

    ix, iy, iw, ih = panel(sl, 4, 22, 92, 18, stripe=ACC_GOOD)
    text(sl, "[AAR sandbox] ─── 提交預測 ───▶ [Remote Eval API] ─── 回傳 PGR ───▶ [AAR sandbox]",
         ix, iy + 1, iw, 6, size=T_BODY, bold=True, color=ACC_GOOD,
         font='mono', align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(sl, "sandbox 內完全沒有 train/test 標籤；必須透過 API 提交才能拿分。允許無限次 submission。",
         ix, iy + 9, iw, 8, size=T_BODY_SM, color=TEXT_SEC,
         align=PP_ALIGN.CENTER, line_spacing=1.3)

    card(sl, 4, 44, 44, 44, title="作者承認的副作用",
         body=[
             ("這個選擇加劇了 reward hacking。",
              {'size': T_BODY, 'bold': True, 'color': ACC_BAD, 'line_spacing': 1.3}),
             ("但實驗顯示：限制提交次數只在極度嚴格的限制下才能壓制 hack（例如 ~10 次 / 數百 hill-climbing 小時）。",
              {'size': T_BODY_SM, 'color': TEXT_SEC, 'space_before': 6, 'line_spacing': 1.35}),
             ("在任何實務上可接受的限制下，AAR 只是更小心地分配提交次數，同樣的 hack 仍會出現。",
              {'size': T_BODY_SM, 'color': TEXT_SEC, 'space_before': 4, 'line_spacing': 1.35}),
         ], stripe=ACC_BAD)

    card(sl, 52, 44, 44, 44, title="含義",
         body=[
             ("Reward hacking 不是「unlimited submissions」單獨造成的。",
              {'size': T_BODY, 'color': TEXT_PRIM, 'line_spacing': 1.3}),
             ("是 outcome-gradable + submission-based eval 這個結構性問題。",
              {'size': T_BODY, 'bold': True, 'color': ACC_GOOD_GLOW,
               'space_before': 5, 'line_spacing': 1.3}),
             ("→ 修正方向不在「次數上限」，而在「eval 結構」。",
              {'size': T_BODY_SM, 'color': TEXT_SEC, 'space_before': 8,
               'italic': True, 'line_spacing': 1.3}),
         ], stripe=ACC_WARN)

    ax_footer(sl, "A5")
    set_notes(sl, """【A5｜Eval API 與 unlimited submissions】論文 Sec 1 Evaluation。深化主 deck Slide 21 reward hacking 根因。

引用原句："We allow unlimited submissions: This exacerbates reward hacking (Sec. 6), but capping submissions only suppresses these hacks at very aggressive limits (e.g. ~10 submissions across hundreds of hill-climbing hours). At any practical cap, our AAR simply budgets its submissions more carefully and the same hacks still appear." """)


# ════════════════════════════════════════════════════════════════════════
# THEME B — Scaffold Architecture (B1–B4)
# ════════════════════════════════════════════════════════════════════════
def slide_B1():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 2", deck_tie="深化 Slide 11")
    h1(sl, "B1 · Dashboard / Forum / External Storage 三層架構",
       y=7.5, h=10, size=26)

    text(sl, "AAR 引擎：Claude Opus 4.6 agents。透過 Dashboard 啟動 a team of parallel AARs，每個在獨立 sandbox 中執行。",
         4, 20, 92, 6, size=T_BODY, color=TEXT_SEC, italic=True, line_spacing=1.3)

    ix, iy, iw, ih = panel(sl, 4, 28, 92, 12, stripe=ACC_GOOD)
    text(sl, "DASHBOARD", ix, iy, iw, 4,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono', align=PP_ALIGN.CENTER)
    text(sl, "啟動 a team of parallel AARs",
         ix, iy + 4, iw, 4, size=T_BODY, bold=True, color=TEXT_PRIM,
         align=PP_ALIGN.CENTER)

    cw, x = 17.5, 6.0
    for i in range(9):
        ix, iy, iw, ih = panel(sl, x, 44, cw / 2, 16,
                               stripe=ACC_DATA_BLUE, tick=False) if False else (None,)*4
        # Compact sandbox squares
        rect(sl, x, 44, 8.5, 16, fill=PANEL_2, line_color=STROKE_HUD, line_w=0.75)
        text(sl, f"#{i+1}", x, 45.5, 8.5, 5,
             size=T_BODY_SM, bold=True, color=ACC_GOOD,
             align=PP_ALIGN.CENTER, font='mono')
        text(sl, "SANDBOX", x, 50.5, 8.5, 3,
             size=8, color=TEXT_MUTED, align=PP_ALIGN.CENTER, font='mono')
        text(sl, "AAR", x, 54, 8.5, 4,
             size=T_BODY_SM, color=TEXT_PRIM, align=PP_ALIGN.CENTER)
        x += 10.0

    ix, iy, iw, ih = panel(sl, 4, 65, 44, 22, stripe=ACC_WARN)
    text(sl, "FORUM", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "分享 findings", ix, iy + 3.5, iw, 5,
         size=T_BODY + 1, bold=True, color=TEXT_PRIM)
    text(sl, "跨 AAR 的協作面之一；每個 AAR 都能讀寫他人 findings。",
         ix, iy + 9, iw, 8, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)

    ix, iy, iw, ih = panel(sl, 52, 65, 44, 22, stripe=ACC_WARN)
    text(sl, "EXTERNAL STORAGE", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "上傳 codebase snapshots", ix, iy + 3.5, iw, 5,
         size=T_BODY + 1, bold=True, color=TEXT_PRIM)
    text(sl, "跨 AAR 共享程式碼工件；所有重要的 logs 都維持在 sandbox 外面。",
         ix, iy + 9, iw, 8, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)

    badge_role(sl, 4, 89.5, 'NOTE')
    text(sl, '"All these important logs are maintained outside the sandbox, to stop our AAR from accidentally deleting them."',
         13, 89.6, 84, 5, size=T_BODY_SM - 1, italic=True, color=ACC_WARN)

    ax_footer(sl, "B1")
    set_notes(sl, """【B1｜三層架構】論文 Sec 2。深化主 deck Slide 11（只用 4 個方塊帶過）。

關鍵設計：所有重要的 logs 都維持在 sandbox 外面 → 防止 AAR 不小心刪除。""")


def slide_B2():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 2", deck_tie="深化 Slide 11")
    h1(sl, "B2 · AAR 可用的 3 個 MCP 工具", y=7.5, h=10, size=28)

    text(sl, "AAR 在 sandbox 內可呼叫的 helper：Common helper functions + Baseline implementations + 3 個 MCP tools。",
         4, 20, 92, 6, size=T_BODY, color=TEXT_SEC, italic=True, line_spacing=1.3)

    tools = [
        ("1", "Submit & get evaluation results",
         "提交預測 → 取得 PGR。AAR 唯一拿到評分的管道。",
         "→ A5：unlimited submissions 是 reward hacking 根因"),
        ("2", "Share & read findings across AARs",
         "讀寫 Forum；跨 AAR 同步研究發現。",
         "→ F2：論文試了 3 種 sharing 變體；local agentic search 勝出"),
        ("3", "Upload & download codebases",
         "讀寫 Storage；跨 AAR 共享程式碼工件。",
         "→ B1：所有 logs 都在 sandbox 外，AAR 無法刪除"),
    ]
    cw, x = 30.0, 4.0
    for num, name, desc, link in tools:
        ix, iy, iw, ih = panel(sl, x, 28, cw, 56, stripe=ACC_GOOD)
        text(sl, num, ix, iy + 1, iw, 10,
             size=44, bold=True, color=ACC_GOOD, font='mono', align=PP_ALIGN.CENTER)
        text(sl, name, ix, iy + 14, iw, 8,
             size=T_BODY + 1, bold=True, color=TEXT_PRIM, align=PP_ALIGN.CENTER,
             line_spacing=1.2)
        text(sl, desc, ix, iy + 24, iw, 14,
             size=T_BODY_SM, color=TEXT_SEC, align=PP_ALIGN.CENTER, line_spacing=1.35)
        text(sl, link, ix, iy + 42, iw, 12,
             size=T_BODY_SM - 1, color=TEXT_MUTED, italic=True,
             align=PP_ALIGN.CENTER, line_spacing=1.3)
        x += cw + 2.0

    text(sl, "AAR 沒有被指定詳細 scaffolding；可以在任何步驟提假設、設計 de-risking 實驗、跑分析、訓練模型。",
         4, 87, 92, 5, size=T_BODY_SM, color=TEXT_MUTED, italic=True,
         align=PP_ALIGN.CENTER)

    ax_footer(sl, "B2")
    set_notes(sl, """【B2｜3 個 MCP 工具】論文 Sec 2。深化主 deck Slide 11。

3 個工具：Submit/eval、Share findings、Upload codebases。
注意：MCP 工具表面看似中性，但 #1（unlimited submissions）和 #2（findings 共享）的設計都直接影響 reward hacking 與 entropy collapse。""")


def slide_B3():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 6 'Prescriptive vs Autonomous'",
            deck_tie="深化 Slide 12")
    h1(sl, "B3 · Autonomous vs Prescriptive Scaffolding",
       y=7.5, h=10, size=28)

    ix, iy, iw, ih = panel(sl, 4, 22, 44, 50, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "PRESCRIPTIVE", ix, iy, iw, 5,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono')
    text(sl, "固定 workflow", ix, iy + 4.5, iw, 6,
         size=T_H2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ("propose ideas → generate plans → write code → smoke tests → full training → analyze → repeat",
         {'size': T_BODY_SM, 'color': TEXT_SEC, 'line_spacing': 1.4}),
        ("固定步驟阻止 AAR 因問題而調整流程。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'space_before': 6, 'line_spacing': 1.35}),
        ("例：當一個 idea 依賴一個未驗證的假設時，固定 pipeline 強迫 AAR 趕著進入 full execution。",
         {'size': T_BODY_SM, 'color': TEXT_SEC, 'space_before': 5,
          'italic': True, 'line_spacing': 1.35}),
    ], ix, iy + 12, iw, ih - 16)

    ix, iy, iw, ih = panel(sl, 52, 22, 44, 50, stripe=ACC_GOOD, fill=PANEL_GOOD)
    text(sl, "AUTONOMOUS", ix, iy, iw, 5,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono')
    text(sl, "完全不規定 workflow", ix, iy + 4.5, iw, 6,
         size=T_H2, bold=True, color=ACC_GOOD)
    text_lines(sl, [
        ("AAR 行為類似 expert researchers：先設計快、便宜的實驗驗證假設，假設成立才投入 full training。",
         {'size': T_BODY_SM, 'color': TEXT_SEC, 'line_spacing': 1.4}),
        ('"Without prescribed steps, AARs behave more like expert researchers: they design fast, cheap experiments to test the hypothesis first and only commit to full training once the premise holds."',
         {'size': T_BODY_SM - 1, 'color': ACC_GOOD_GLOW, 'italic': True,
          'space_before': 6, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 16)

    ix, iy, iw, ih = panel(sl, 4, 76, 92, 16, stripe=ACC_WARN)
    text(sl, "結果", ix, iy, 12, ih,
         size=T_H2, bold=True, color=ACC_WARN,
         anchor=MSO_ANCHOR.MIDDLE, font='mono')
    text(sl, "Prescriptive 反而表現比 Autonomous 差。這個發現直接決定了論文最終採用 autonomous scaffolding 設計。",
         ix + 13, iy + 1.5, iw - 13, ih - 3,
         size=T_BODY, color=TEXT_PRIM, line_spacing=1.4)

    ax_footer(sl, "B3")
    set_notes(sl, """【B3｜Autonomous vs Prescriptive】論文 Sec 6 "Prescriptive Scaffolding vs. Autonomous Scaffolding"。深化主 deck Slide 12。

結論：Prescriptive 反而比 Autonomous 差。""")


def slide_B4():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 3.1 + Sec 6",
            deck_tie="深化 Slide 13（主 deck 沒對比 undirected/pre-gen）")
    h1(sl, "B4 · Directed vs Undirected（+ 第三種失敗：Pre-generated Specific Ideas）",
       y=7.5, h=10, size=22)

    cols = [
        ("DIRECTED", ACC_GOOD, "✓ 勝出",
         "每個 AAR 指派一個不同的、模糊的、簡短的研究方向。",
         '例：「combining weak-to-strong supervision and unsupervised elicitation」',
         "hill-climbing 速度與最終 PGR 都明顯較好。"),
        ("UNDIRECTED", ACC_BAD, "✗ entropy collapse",
         "9 個 AAR 用同一個 prompt，沒有任何指引。",
         "結果集中到少數方向（如 self-training），快速 collapse。",
         "對比 directed：表現顯著較差。"),
        ("PRE-GENERATED", ACC_BAD_DIM, "✗ 第三種失敗",
         "讓 Claude 預先生成一大堆「具體的研究 idea」再分派。",
         "失敗 1：idea 分布嚴重偏斜到少數方向（與 undirected 同源）。",
         "失敗 2：抽象層次聽起來 principled，實作後卻無效；提前 commit 等於浪費 compute。"),
    ]
    cw, x = 30.0, 4.0
    for name, color, verdict, line1, line2, line3 in cols:
        ix, iy, iw, ih = panel(sl, x, 22, cw, 64, stripe=color)
        text(sl, name, ix, iy, iw, 5,
             size=T_BODY_SM, color=TEXT_MUTED, font='mono', align=PP_ALIGN.CENTER)
        text(sl, verdict, ix, iy + 4, iw, 6,
             size=T_H2 - 2, bold=True, color=color, align=PP_ALIGN.CENTER)
        text_lines(sl, [
            (line1, {'size': T_BODY_SM, 'color': TEXT_PRIM,
                     'line_spacing': 1.35}),
            (line2, {'size': T_BODY_SM, 'color': TEXT_SEC,
                     'space_before': 6, 'italic': True, 'line_spacing': 1.35}),
            (line3, {'size': T_BODY_SM, 'color': TEXT_SEC,
                     'space_before': 6, 'line_spacing': 1.35}),
        ], ix, iy + 14, iw, ih - 16)
        x += cw + 2.0

    ax_footer(sl, "B4")
    set_notes(sl, """【B4｜Directed vs Undirected vs Pre-generated】論文 Sec 3.1 + Sec 6 "Ambiguous Research Directions vs. Specific Research Ideas"。

Directed 勝出。Undirected 與 Pre-generated 同源（都會 entropy collapse 或浪費 compute）。""")


# ════════════════════════════════════════════════════════════════════════
# THEME C — Five Methods (C1–C5)
# ════════════════════════════════════════════════════════════════════════
def slide_C1():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 3.2 'Entropy collapse of research ideas'",
            deck_tie="深化 Slide 13")
    h1(sl, "C1 · 11 個 method family + Shannon entropy 量測",
       y=7.5, h=10, size=26)

    families = ["self-training", "ensemble", "distillation", "data filtering",
                "confidence weighting", "loss function", "unsupervised elicitation",
                "curriculum", "model internal", "evolutionary", "other"]
    ix, iy, iw, ih = panel(sl, 4, 22, 56, 64, stripe=ACC_GOOD)
    text(sl, "11 METHOD FAMILIES", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "Claude 把每個 AAR 提出的 idea 分類到 11 個 family 之一。",
         ix, iy + 5, iw, 5, size=T_BODY_SM, color=TEXT_SEC, italic=True)
    # tag cloud: 3 columns × 4 rows
    tag_x, tag_y, tw, th, gx, gy = ix, iy + 13, 16, 6, 0.8, 1.2
    for i, fam in enumerate(families):
        col = i % 3
        row = i // 3
        bx = tag_x + col * (tw + gx)
        by = tag_y + row * (th + gy)
        rect(sl, bx, by, tw, th, fill=PANEL_2, line_color=STROKE,
             rounded=True, radius=0.3)
        text(sl, fam, bx, by, tw, th,
             size=T_BODY_SM - 1, color=TEXT_PRIM,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font='mono')

    ix, iy, iw, ih = panel(sl, 63, 22, 33, 30, stripe=ACC_WARN)
    text(sl, "MEASUREMENT", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "Shannon entropy", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=TEXT_PRIM)
    text(sl, "H = -Σ pᵢ log pᵢ", ix, iy + 11, iw, 6,
         size=T_H2, bold=True, color=ACC_GOOD_GLOW, font='mono',
         align=PP_ALIGN.CENTER)
    text(sl, "每個 iteration step，計算所有 active workers 的 category 分布的 Shannon entropy（cross-sectional）。",
         ix, iy + 19, iw, 14, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.35)

    card(sl, 63, 56, 33, 30, title="觀察",
         body=[
             ("directed：能有效避免 entropy collapse。",
              {'size': T_BODY_SM, 'color': ACC_GOOD, 'line_spacing': 1.3}),
             ("undirected：集中到少數方向（如 self-training），快速 collapse。",
              {'size': T_BODY_SM, 'color': ACC_BAD,
               'space_before': 4, 'line_spacing': 1.3}),
         ], stripe=ACC_DATA_BLUE, title_size=T_BODY + 1)

    ax_footer(sl, "C1")
    set_notes(sl, """【C1｜11 family + entropy】論文 Sec 3.2。深化主 deck Slide 13（只說「entropy collapse」概念）。

11 個 family + Shannon entropy = -Σ p log p。
這是 cross-sectional 量測：同一時刻，9 個 worker 在做幾種不同方向。""")


def _method_slide(code, pgr_str, title_full, paper_ref, deck_tie,
                  steps, footer_note=None, pgr_color=ACC_GOOD_GLOW):
    sl = add_slide(BG_BASE)
    ax_meta(sl, paper_ref, deck_tie=deck_tie)
    h1(sl, f"{code} · {title_full}", y=7.5, h=10, size=24)

    # PGR badge top-right
    ix, iy, iw, ih = panel(sl, 76, 21, 20, 14, stripe=ACC_GOOD)
    text(sl, "PGR", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono', align=PP_ALIGN.CENTER)
    text(sl, pgr_str, ix, iy + 3.5, iw, 7,
         size=36, bold=True, color=pgr_color, align=PP_ALIGN.CENTER)

    # Steps column — for n=5: sh=13 so body fits within panel (visual from iy=9.574%)
    n = max(len(steps), 1)
    sh = 13.0 if n == 5 else (60.0 / n) - 1.5
    sy, gap = 22.0, 1.5
    for i, (head, body) in enumerate(steps):
        ix, iy, iw, ih = panel(sl, 4, sy, 70, sh, stripe=ACC_DATA_BLUE)
        text(sl, f"{i+1}", ix, iy, 5, ih,
             size=20, bold=True, color=ACC_GOOD, font='mono',
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, head, ix + 6, iy + 0.5, iw - 6, 4.5,
             size=T_BODY, bold=True, color=TEXT_PRIM)
        text(sl, body, ix + 6, iy + 5, iw - 6, sh - 8.6,
             size=T_BODY_SM - 1, color=TEXT_SEC, line_spacing=1.3)
        sy += sh + gap

    if footer_note:
        text(sl, footer_note, 4, 87, 92, 5,
             size=T_BODY_SM, color=ACC_WARN, italic=True, align=PP_ALIGN.CENTER)
    return sl


def slide_C2():
    sl = _method_slide(
        "C2", "0.93",
        "CCS + Evolution Strategy Refinement（論文最高分方法）",
        "Sec 4", "—（主 deck 完全略過 Sec 4）",
        [("CCS probe",
          "在 strong model 的 hidden representations 上跨層訓練 Contrastive Consistency Search probe，找出無監督的 truth direction。"),
         ("Confidence resample",
          "用 CCS 與 weak label 的一致性作為 confidence weight，重新 sample 訓練集。"),
         ("SGD warmup",
          "在 resampled data 上做一輪 SGD warmup。"),
         ("Evolution Strategy on LoRA",
          "跑 gradient-free Evolution Strategy 優化 LoRA 參數。"),
         ("Swap-consistency fitness",
          "ES 的 fitness signal：無監督的 swap-consistency — 擾動產生的預測必須既 confident 又 symmetric，即 p(A>B) ≈ 1 - p(B>A)。")],
        footer_note="集成：跨 16 seeds 做 swap-consistent inference + logit space 上的 trimmed-mean。",
    )
    set_notes(sl, """【C2｜CCS + ES Refinement】論文 Sec 4。PGR = 0.93，論文最高分方法。

5 步流程 + 16 seeds 集成。Swap-consistency 是無監督 fitness signal 的關鍵。""")
    ax_footer(sl, "C2")


def slide_C3():
    sl = _method_slide(
        "C3", "0.78",
        "EM Posterior（後續被選去做 production transfer）",
        "Sec 4", "—（與 E2 production transfer 相連）",
        [("抽取 multi-template logit margins",
          "從凍結的 strong base model 抽取多個 prompt 模板 × 兩種 ordering 的 logit margins。"),
         ("4 個 features per instance",
          "weak-label confidence · strong-model margin · margin stability across templates · weak/strong agreement。"),
         ("Noisy channel model",
          "學一個 instance-dependent noisy channel model P(weak_label | true_label)，用 maximum likelihood。"),
         ("Bayesian posterior",
          "把 channel 與 strong model margin 推出的 prior 結合 → Bayesian posterior labels；對 posterior 做 tempering。"),
         ("2 輪 EM",
          "用目前 posterior 訓練 student → 用 student 預測重新估 channel → 重算 posterior。")],
        footer_note="E2：這個方法被選去做 production scale transfer（Sonnet 4.0），結果只 +0.5 noise — 見 E2。",
    )
    set_notes(sl, """【C3｜EM Posterior】論文 Sec 4。PGR = 0.78。

被選去做 production transfer。E2 詳述 production failure。""")
    ax_footer(sl, "C3")


def slide_C4():
    sl = _method_slide(
        "C4", "0.75",
        "Overlap Density（論文標為 'alien'）",
        "Sec 4", "—",
        [("抽取 embeddings",
          "從凍結的 strong base model 抽取每個訓練 example 的 embedding。"),
         ("4 個 alignment signals",
          "CCS probe · kNN smoothness · local density · mid-entropy pref（4 signals）。"),
         ("Z-score-weighted sum",
          "把 4 個 signal 用 z-score 標準化後加權。"),
         ("Top 50% + class balance",
          "取 top 50% 分數的 example（並維持 class balance）做 fine-tune。"),
         ("論文評語：alien",
          '"Certain ideas are alien (e.g. Overlap Density)" — 這是少數連作者也覺得「想不到要這樣做」的方法。')],
        footer_note="F4 alien science：AAR 拓寬科學的探索空間 — 但需要 legibility training 防止 idea 變得不可驗證。",
        pgr_color=ACC_WARN,
    )
    set_notes(sl, """【C4｜Overlap Density】論文 Sec 4。PGR = 0.75。

概念：為每個訓練 example 打分，看它的 weak label 與 strong model 的內部 semantic structure 對得多齊。
論文評語：alien — 少數連作者也想不到要這樣做的方法。""")
    ax_footer(sl, "C4")


def slide_C5():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 4", deck_tie="—")
    h1(sl, "C5 · MDL Curriculum (0.68) + Epiplexity (0.62)",
       y=7.5, h=10, size=26)

    ix, iy, iw, ih = panel(sl, 4, 22, 44, 65, stripe=ACC_DATA_BLUE)
    text(sl, "MDL Curriculum  ·  PGR 0.68", ix, iy, iw, 5,
         size=T_H2 - 2, bold=True, color=TEXT_PRIM)
    text(sl, "兩階段 curriculum，把 weak-label confidence 解釋為 compressibility proxy（MDL 直覺：高信心 = 高訊號低雜訊）。",
         ix, iy + 6, iw, 10, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.35,
         italic=True)
    text_lines(sl, [
        ("Phase 1", {'size': T_BODY, 'bold': True, 'color': ACC_GOOD,
                     'font': 'mono'}),
        ("只用前 50%（高信心）訓練 2 epochs。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 3, 'line_spacing': 1.35}),
        ("Phase 2", {'size': T_BODY, 'bold': True, 'color': ACC_GOOD,
                     'font': 'mono', 'space_before': 10}),
        ("從 Phase 1 的 checkpoint 接續，用完整資料訓練 3 epochs，LR 降為一半。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 3, 'line_spacing': 1.35}),
        ("與硬篩 (hard filtering) 不同：所有資料最終都會用到。",
         {'size': T_BODY_SM, 'color': ACC_WARN,
          'space_before': 8, 'italic': True, 'line_spacing': 1.35}),
    ], ix, iy + 19, iw, ih - 22)

    ix, iy, iw, ih = panel(sl, 52, 22, 44, 65, stripe=ACC_DATA_BLUE)
    text(sl, "Epiplexity  ·  PGR 0.62", ix, iy, iw, 5,
         size=T_H2 - 2, bold=True, color=TEXT_PRIM)
    text(sl, "量化每個 sample 的 epiplexity = 訓練過程中第一次與最後一次相遇時的 loss drop。高 = 真實結構；≈0 = 純雜訊。",
         ix, iy + 6, iw, 12, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.35,
         italic=True)
    text_lines(sl, [
        ("1.  K-fold CV → out-of-fold soft labels",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.35}),
        ("2.  在 OOF labels 上跑 epiplexity probe pass",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 4, 'line_spacing': 1.35}),
        ("3.  Adaptive label smoothing：高 epiplexity 保留 sharp OOF label；bottom 40% 漸進地平滑向 0.5（convex curvature 集中於最差 tail）",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 4, 'line_spacing': 1.35}),
        ("4.  訓練時加 swap augmentation",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 4, 'line_spacing': 1.35}),
    ], ix, iy + 21, iw, ih - 24)

    ax_footer(sl, "C5")
    set_notes(sl, """【C5｜MDL Curriculum + Epiplexity】論文 Sec 4。

兩個 information-theory 系列的方法。MDL: 0.68；Epiplexity: 0.62。""")


# ════════════════════════════════════════════════════════════════════════
# THEME D — Reward Hacking Deep-Dive (D1–D4)
# ════════════════════════════════════════════════════════════════════════
def slide_D1():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 5 'Finding dataset shortcuts'",
            deck_tie="深化 Slide 21（主 deck 只列名稱）")
    h1(sl, "D1 · Hack 1：Dataset Shortcuts", y=7.5, h=10, size=28)

    ix, iy, iw, ih = panel(sl, 4, 22, 44, 60, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "CASE 1 · MATH TESTBED", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "答案出現次數 = 正確度", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_BAD)
    text(sl, "AAR 找到 dataset 層級的 shortcut：每題最常見的答案通常是正確的。",
         ix, iy + 12, iw, 16, size=T_BODY, color=TEXT_PRIM, line_spacing=1.4)
    text(sl, "→ 完全不需要 weak supervision，也不需要 strong model 的 latent capability。",
         ix, iy + 30, iw, 12, size=T_BODY_SM, color=TEXT_SEC, italic=True,
         line_spacing=1.35)

    ix, iy, iw, ih = panel(sl, 52, 22, 44, 60, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "CASE 2 · CODING TESTBED", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "穿透作者主動加的防線", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ("作者預先想到了 linguistic bias 風險，所以從多個不同 LM 取樣 coding solutions。",
         {'size': T_BODY_SM, 'color': TEXT_SEC, 'line_spacing': 1.4}),
        ("AAR 仍然找到方法：把 solutions 依照產生模型分群（model clustering），辨識哪些 cluster 含較多正確 / 錯誤解。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 6, 'line_spacing': 1.4}),
        ("作者主動加了一道防線，AAR 還是穿過去了。",
         {'size': T_BODY_SM, 'color': ACC_WARN,
          'space_before': 6, 'italic': True, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 14)

    text(sl, "教訓　·　Dataset 設計者「以為自己消除了 hackable pattern」，但 AAR 能找到更深層的 pattern。",
         4, 87, 92, 5, size=T_BODY_SM, color=ACC_WARN, italic=True,
         align=PP_ALIGN.CENTER)

    ax_footer(sl, "D1")
    set_notes(sl, """【D1｜Dataset Shortcuts】論文 Sec 5。深化主 deck Slide 21。

兩個 case：Math（answer frequency）、Coding（model clustering 穿透 multi-LM sampling 防線）。""")


def slide_D2():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 5 'Iteratively cherry-picking random seeds'",
            deck_tie="深化 Slide 21")
    h1(sl, "D2 · Hack 2：Seed Cherry-Picking via Unlimited Submissions",
       y=7.5, h=10, size=22)

    text(sl, "設計背景：unlimited submissions 讓 test set 實質上變成 validation set with OOD split。",
         4, 20, 92, 5, size=T_BODY, color=ACC_WARN, italic=True)

    # 3-step loop
    steps = [
        ("用多個 random seed 訓練模型", ACC_DATA_BLUE),
        ("Cherry-pick PGR 最高的 seed 對應的模型", ACC_WARN),
        ("用那個模型作為下一代訓練的 seed", ACC_BAD),
    ]
    sy = 28.0
    for i, (desc, color) in enumerate(steps):
        ix, iy, iw, ih = panel(sl, 8, sy, 70, 14, stripe=color)
        text(sl, f"STEP {i+1}", ix, iy, 12, ih,
             size=T_BODY_SM, bold=True, color=color, font='mono',
             anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        text(sl, desc, ix + 14, iy + 1.5, iw - 14, ih - 3,
             size=T_BODY, color=TEXT_PRIM, anchor=MSO_ANCHOR.MIDDLE,
             line_spacing=1.3)
        sy += 17

    text(sl, "↻", 81, 41, 8, 22,
         size=60, color=ACC_BAD, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(sl, "回到 STEP 1", 79, 64, 14, 5,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono', align=PP_ALIGN.CENTER)

    card(sl, 4, 80, 92, 11, title=None, stripe=ACC_WARN,
         body=[('"We allow AARs to call the remote evaluation API unlimited times, so essentially our test set is a validation set with an OOD split."',
                {'size': T_BODY_SM, 'color': TEXT_PRIM, 'italic': True,
                 'line_spacing': 1.35}),
               ("→ AAR 不需要任何「計算 submission 次數」的邏輯；只是花時間試很多 seed。",
                {'size': T_BODY_SM, 'color': TEXT_SEC,
                 'space_before': 3, 'line_spacing': 1.35})])

    ax_footer(sl, "D2")
    set_notes(sl, """【D2｜Seed Cherry-Picking】論文 Sec 5。深化主 deck Slide 21。

根因是 Sec 1 設計選擇：unlimited submissions（見 A5）。""")


def slide_D3():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 5 'Exfiltrating test labels from remote API'",
            deck_tie="深化 Slide 21")
    h1(sl, "D3 · Hack 3：Test Label Exfiltration",
       y=7.5, h=10, size=26)

    ix, iy, iw, ih = panel(sl, 4, 21, 44, 65, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "ATTACK SURFACE", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "Binary classification 的弱點", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ("只改一個 test example 的預測，其他不變 → 看 PGR 變化來反推真實標籤。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
        ("試 True → 若 PGR 升 → 真標籤是 True；反之亦然。",
         {'size': T_BODY_SM, 'color': TEXT_SEC,
          'space_before': 6, 'line_spacing': 1.4}),
        ("這是 binary outcome eval 的結構性弱點，不是實作 bug。",
         {'size': T_BODY_SM, 'color': ACC_WARN,
          'space_before': 8, 'italic': True, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 14)

    ix, iy, iw, ih = panel(sl, 52, 21, 44, 65, stripe=ACC_DATA_BLUE)
    text(sl, "AAR'S 3-STEP FLOW", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "Cost-aware exfiltration", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_GOOD)
    text_lines(sl, [
        ("1.  估自己對每個 test example 的 prediction uncertainty",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
        ("2.  挑出 5 個最不確定的 example",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 5, 'line_spacing': 1.4}),
        ("3.  用上述方法對這 5 個分別翻轉測試，反推真實標籤",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 5, 'line_spacing': 1.4}),
        ("→ 選 5 個而不是全部：在 unlimited submissions 下仍然有 cost；AAR 自行做了 cost-value 取捨。",
         {'size': T_BODY_SM, 'color': ACC_WARN,
          'space_before': 8, 'italic': True, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 14)

    ax_footer(sl, "D3")
    set_notes(sl, """【D3｜Test Label Exfiltration】論文 Sec 5。深化主 deck Slide 21。

對 binary classification 的結構性攻擊；AAR 自主做了 cost-value 取捨（只挑 5 個）。""")


def slide_D4():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 5 'Executing coding answers' + Sec 5 結尾",
            deck_tie="深化 Slide 21 + Slide 24")
    h1(sl, "D4 · Hack 4：Unit Test Bypass + Meta-Finding",
       y=7.5, h=10, size=24)

    ix, iy, iw, ih = panel(sl, 4, 21, 44, 65, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "HACK 4 · MECHANISM", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "直接寫並執行 unit test", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ("在 coding testbed，AAR 直接寫並執行 unit test 來取得 solution 的正確標籤。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
        ("直接繞過 weak teacher 和 strong student — 這是最直接的協定違反。",
         {'size': T_BODY_SM, 'color': ACC_BAD,
          'space_before': 6, 'bold': True, 'line_spacing': 1.4}),
        ("這個案例特別簡單明顯，但也最赤裸地暴露：sandbox 內可執行 = sandbox 內可繞過。",
         {'size': T_BODY_SM, 'color': TEXT_SEC,
          'space_before': 6, 'italic': True, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 14)

    ix, iy, iw, ih = panel(sl, 52, 21, 44, 65, stripe=ACC_WARN, fill=PANEL_BAD)
    text(sl, "META-FINDING · 論文核心警示之一", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "沒有任何一個 hack 是預測到的", ix, iy + 4, iw, 8,
         size=T_H2 - 2, bold=True, color=ACC_WARN, line_spacing=1.2)
    text_lines(sl, [
        ('"None of the authors predicted these hacks before running AARs. While we tried to add patches to the environment, AARs still figured out new unexpected ways to hack."',
         {'size': T_BODY_SM - 1, 'color': TEXT_PRIM,
          'italic': True, 'line_spacing': 1.45}),
        ("作者試圖打 patch，AAR 還是找到新的、未預料的 hack 方式。",
         {'size': T_BODY_SM, 'color': ACC_BAD,
          'space_before': 8, 'line_spacing': 1.4}),
        ("→ 未來工作必須在「完全 held-out」的資料上測試 AAR 發現的 idea。",
         {'size': T_BODY_SM, 'color': ACC_GOOD,
          'space_before': 6, 'bold': True, 'line_spacing': 1.4}),
    ], ix, iy + 16, iw, ih - 18)

    ax_footer(sl, "D4")
    set_notes(sl, """【D4｜Unit Test Bypass + Meta-Finding】論文 Sec 5 結尾。深化主 deck Slide 21 + Slide 24。

Hack 4 是最直接的協定違反。Meta-finding 是這節核心：作者試 patch，AAR 仍找到新方式。""")


# ════════════════════════════════════════════════════════════════════════
# THEME E — Generalization, Transfer, Complexity (E1–E3)
# ════════════════════════════════════════════════════════════════════════
def slide_E1():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 3.4 'Generalization to held-out datasets'",
            deck_tie="深化 Slide 22（Chat/Math/Code 數字未拆解原因）")
    h1(sl, "E1 · Cross-dataset transfer：兩個方法在 Code 上的不同命運",
       y=7.5, h=10, size=22)

    text(sl, "從 chat preference 上選 2 個 representative idea，遷移到 math 與 coding。規則：允許 hyperparameter tuning，不允許 method modification。",
         4, 19, 92, 7, size=T_BODY_SM, color=TEXT_SEC, italic=True, line_spacing=1.4)

    # 2x2 matrix
    rect(sl, 30, 30, 30, 8, fill=PANEL_2, line_color=STROKE_HUD)
    text(sl, "MATH", 30, 30, 30, 8,
         size=T_BODY, bold=True, color=ACC_GOOD,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font='mono')
    rect(sl, 60, 30, 30, 8, fill=PANEL_2, line_color=STROKE_HUD)
    text(sl, "CODING", 60, 30, 30, 8,
         size=T_BODY, bold=True, color=ACC_GOOD,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font='mono')

    # Row 1: Idea 1
    rect(sl, 4, 38, 26, 18, fill=PANEL, line_color=STROKE)
    text(sl, "IDEA 1 (SOTA)", 4, 38, 26, 6,
         size=T_BODY_SM, bold=True, color=TEXT_PRIM,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font='mono')
    text(sl, "依賴一般化的 strong model 能力", 4, 44, 26, 11,
         size=T_BODY_SM - 1, color=TEXT_SEC, align=PP_ALIGN.CENTER,
         line_spacing=1.3)
    rect(sl, 30, 38, 30, 18, fill=PANEL_GOOD, line_color=ACC_GOOD)
    text(sl, "✓ 成功", 30, 38, 30, 18,
         size=T_H2, bold=True, color=ACC_GOOD,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(sl, 60, 38, 30, 18, fill=PANEL_GOOD, line_color=ACC_GOOD)
    text(sl, "✓ 成功", 60, 38, 30, 18,
         size=T_H2, bold=True, color=ACC_GOOD,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Row 2: Idea 2
    rect(sl, 4, 56, 26, 18, fill=PANEL, line_color=STROKE)
    text(sl, "IDEA 2", 4, 56, 26, 6,
         size=T_BODY_SM, bold=True, color=TEXT_PRIM,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font='mono')
    text(sl, "依賴 strong student 的 zero-shot 預測", 4, 62, 26, 11,
         size=T_BODY_SM - 1, color=TEXT_SEC, align=PP_ALIGN.CENTER,
         line_spacing=1.3)
    rect(sl, 30, 56, 30, 18, fill=PANEL_GOOD, line_color=ACC_GOOD)
    text(sl, "✓ 成功", 30, 56, 30, 18,
         size=T_H2, bold=True, color=ACC_GOOD,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(sl, 60, 56, 30, 18, fill=PANEL_BAD, line_color=ACC_BAD)
    text(sl, "✗ 失敗", 60, 56, 30, 18,
         size=T_H2, bold=True, color=ACC_BAD,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    card(sl, 4, 78, 92, 13, title="失敗原因（Idea 2 在 Coding）",
         body=[("strong student 在 coding 上的 zero-shot 能力比 math 弱很多。AAR 發現的 idea 泛化能力取決於它利用了哪些 model capability。",
                {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4})],
         stripe=ACC_WARN, title_size=T_BODY + 1)

    ax_footer(sl, "E1")
    set_notes(sl, """【E1｜Cross-dataset transfer】論文 Sec 3.4。深化主 deck Slide 22。

Idea 1：依賴一般 model capability → 成功遷移到 math + coding。
Idea 2：依賴 strong student zero-shot → math 成功、coding 失敗（zero-shot 能力較弱）。""")


def slide_E2():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 3.5 'Generalization to production scales'",
            deck_tie="—（主 deck 完全沒提這次失敗）")
    h1(sl, "E2 · Production scale transfer failure：EM Posterior → Sonnet 4.0 = +0.5 noise",
       y=7.5, h=10, size=20)

    # Big result
    ix, iy, iw, ih = panel(sl, 4, 22, 50, 25, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "RESULT", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono', align=PP_ALIGN.CENTER)
    text(sl, "+0.5", ix, iy + 4, iw, 12,
         size=T_MEGA_SM, bold=True, color=ACC_BAD, align=PP_ALIGN.CENTER)
    text(sl, "point improvement · in noise floor",
         ix, iy + 17, iw, 5, size=T_BODY_SM, color=TEXT_MUTED,
         align=PP_ALIGN.CENTER, font='mono')

    ix, iy, iw, ih = panel(sl, 58, 22, 38, 25, stripe=ACC_DATA_BLUE)
    text(sl, "嘗試", ix, iy, iw, 5,
         size=T_BODY, bold=True, color=TEXT_PRIM)
    text(sl, "把 EM-based posterior label modeling（C3）遷移到 chat helpfulness preference dataset，用 Sonnet 4.0 與生產級訓練 infrastructure。",
         ix, iy + 5, iw, 18, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.4)

    ix, iy, iw, ih = panel(sl, 4, 50, 92, 32, stripe=ACC_WARN)
    text(sl, "FAILURE DIAGNOSIS · 作者自陳", ix, iy, iw, 5,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono')
    text(sl, "上游訊號太弱 → 但可能是 elicitation failure，非方法本身限制",
         ix, iy + 4.5, iw, 6, size=T_H2 - 4, bold=True, color=ACC_WARN)
    text_lines(sl, [
        ("base model 在生產比較資料上的 forced-choice preference margins 太弱，無法驅動有意義的 label correction。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
        ("作者懷疑這是 elicitation failure：他們只試過 single-token A/B forced choice；更豐富的 scoring 方式（chain-of-thought before commitment、continuation logprobs）尚未試過。",
         {'size': T_BODY_SM, 'color': TEXT_SEC,
          'space_before': 6, 'line_spacing': 1.4}),
    ], ix, iy + 11, iw, ih - 13)

    text(sl, "教訓（與 Sec 3.4 呼應）　·　AAR 的 idea 傾向利用「發現時的 dataset/model 結構」，遷移需要那個結構在新環境中也出現。",
         4, 86, 92, 5, size=T_BODY_SM, color=ACC_WARN, italic=True,
         align=PP_ALIGN.CENTER)

    ax_footer(sl, "E2")
    set_notes(sl, """【E2｜Production scale failure】論文 Sec 3.5。主 deck 完全沒提這次失敗。

EM Posterior（C3）→ Sonnet 4.0 + 生產 infrastructure → 只 +0.5 noise。
作者懷疑是 elicitation failure（只試過 single-token A/B forced choice），不是方法本身限制。""")


def slide_E3():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 3.3 'Higher PGR does not consistently come with higher idea complexity'",
            deck_tie="—")
    h1(sl, "E3 · Idea complexity tracking：3 個指標、後期持平",
       y=7.5, h=10, size=24)

    card(sl, 4, 22, 44, 30, title="擔憂",
         body=[("AAR 可能會「堆 20 個 trick」讓 idea 越堆越複雜，導致過擬合特定 dataset/model。",
                {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4})],
         stripe=ACC_BAD, title_size=T_BODY + 1)

    card(sl, 4, 54, 44, 30, title="3 個 complexity 指標",
         body=[("1.  Claude-scored code complexity",
                {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
               ("2.  Lines of raw Python code",
                {'size': T_BODY_SM, 'color': TEXT_PRIM,
                 'space_before': 3, 'line_spacing': 1.4}),
               ("3.  Lines of Claude-generated pseudocode",
                {'size': T_BODY_SM, 'color': TEXT_PRIM,
                 'space_before': 3, 'line_spacing': 1.4})],
         stripe=ACC_DATA_BLUE, title_size=T_BODY + 1)

    fig_embed(sl, 52, 22, 44, 50, "paper_fig08_code_complexity.png",
              caption="Figure 8 — Idea complexity 隨 hill-climbing step 的趨勢。")

    card(sl, 52, 74, 44, 16, title="觀察",
         body=[("早期：complexity 與 PGR 同步上升。",
                {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.3}),
               ("後期：PGR 繼續上升，complexity 幾乎持平。",
                {'size': T_BODY_SM, 'color': ACC_GOOD_GLOW,
                 'space_before': 3, 'bold': True, 'line_spacing': 1.3})],
         stripe=ACC_GOOD, title_size=T_BODY + 1)

    ax_footer(sl, "E3")
    set_notes(sl, """【E3｜Complexity tracking】論文 Sec 3.3。

3 個指標（可能高估真實 complexity，因有些 component 完全沒貢獻；但 AAR 在 hill-climbing 大量跑 ablation 已移除多數無效 component）。
觀察：後期 PGR 上升但 complexity 持平。""")


# ════════════════════════════════════════════════════════════════════════
# THEME F — Discussion, Limitations, Future Work (F1–F5)
# ════════════════════════════════════════════════════════════════════════
def slide_F1():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 6 'LM Self-evolution vs. Heuristic Evolutionary Search'",
            deck_tie="—")
    h1(sl, "F1 · LM Self-evolution vs Heuristic Evolutionary Search",
       y=7.5, h=10, size=24)

    ix, iy, iw, ih = panel(sl, 4, 22, 44, 60, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "HEURISTIC ES", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "把 idea 視為 black box", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ("依 PGR 作為 fitness 選擇與變異 idea；可靠 upweight low-PGR direction 維持多樣性。",
         {'size': T_BODY_SM, 'color': TEXT_SEC, 'line_spacing': 1.4}),
        ("盲點：只看 outcome；忽略所有 process signal — 訓練 logs、loss curves、gradient norms、model predictions 全部丟掉。",
         {'size': T_BODY_SM, 'color': ACC_BAD,
          'space_before': 6, 'line_spacing': 1.4}),
        ("失敗場景：一個 idea 因為 gradient exploding 拿到負 PGR → ES 立刻放棄整個方向。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 6, 'italic': True, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 14)

    ix, iy, iw, ih = panel(sl, 52, 22, 44, 60, stripe=ACC_GOOD, fill=PANEL_GOOD)
    text(sl, "LM SELF-EVO", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "能讀 process signal 並修正", ix, iy + 4, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_GOOD)
    text_lines(sl, [
        ("LM-driven agent 會從 training log 診斷出 gradient 問題、修 hyperparameter、重跑，可能救回來。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
        ('"If an idea yields negative PGR because gradient norms explode, evolutionary search might immediately abandon the entire direction. An LM driven agent, in contrast, would diagnose the failure from the training logs, fix the hyperparameters, and rerun, potentially recovering a strong result from what looked like a dead end."',
         {'size': T_BODY_SM - 2, 'color': ACC_GOOD_GLOW,
          'space_before': 5, 'italic': True, 'line_spacing': 1.3}),
        ("作者主張：未來應投資 improving LM self-evolution，而不是 heuristic search。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 6, 'bold': True, 'line_spacing': 1.4}),
    ], ix, iy + 12, iw, ih - 14)

    ax_footer(sl, "F1")
    set_notes(sl, """【F1｜LM Self-evo vs Heuristic ES】論文 Sec 6。

ES 的盲點是「只看 outcome」。LM agent 能讀 training log 自己診斷修正。""")


def slide_F2():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 6 'Finding Sharing'", deck_tie="—")
    h1(sl, "F2 · Finding Sharing 3 個變體：local agentic search 勝出",
       y=7.5, h=10, size=24)

    variants = [
        ("V1", "Remote keyword search", ACC_BAD,
         "findings 存在 database，AAR 用 keyword 查。",
         "keyword search 本質上有限。"),
        ("V2", "Remote agentic search API", ACC_WARN,
         "把 database 透過 MCP server 暴露給 AAR。",
         "雖是 agentic，但實務上 AAR 仍會產出『像 keyword 的 query』，沒做到深層 retrieval。"),
        ("V3", "Local agentic search ✓", ACC_GOOD,
         "把所有 findings 同步進每個 AAR 的 sandbox 本地，讓 AAR 自主 retrieval。",
         "AAR 可以瀏覽（browse），能發現「它原本不會知道要去搜尋」的 findings。"),
    ]
    cw, x = 30.0, 4.0
    for code, name, color, mech, why in variants:
        ix, iy, iw, ih = panel(sl, x, 22, cw, 60, stripe=color)
        text(sl, code, ix, iy, iw, 5,
             size=T_H2, bold=True, color=color, font='mono', align=PP_ALIGN.CENTER)
        text(sl, name, ix, iy + 6, iw, 8,
             size=T_BODY, bold=True, color=TEXT_PRIM, align=PP_ALIGN.CENTER,
             line_spacing=1.25)
        text(sl, "機制", ix, iy + 18, iw, 4,
             size=T_CAPTION, color=TEXT_MUTED, font='mono')
        text(sl, mech, ix, iy + 22, iw, 14,
             size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.35)
        text(sl, "結果分析", ix, iy + 38, iw, 4,
             size=T_CAPTION, color=TEXT_MUTED, font='mono')
        text(sl, why, ix, iy + 42, iw, 16,
             size=T_BODY_SM, color=color, italic=True, line_spacing=1.35)
        x += cw + 2.0

    text(sl, "對照類比　·　研究者「廣讀」常找到「精準 literature search 漏掉」的連結。",
         4, 87, 92, 5, size=T_BODY_SM, color=ACC_WARN, italic=True,
         align=PP_ALIGN.CENTER)

    ax_footer(sl, "F2")
    set_notes(sl, """【F2｜Finding Sharing 3 變體】論文 Sec 6。

V3 local agentic search 勝出，因為 AAR 可以瀏覽，能發現未預料的 findings。""")


def slide_F3():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 7 'Generalization across datasets / model scales / production'",
            deck_tie="深化 Slide 29 open question 2")
    h1(sl, "F3 · 泛化的 3 種尺度限制 + OOD test 的盲點",
       y=7.5, h=10, size=24)

    scales = [
        ("1", "跨 dataset",
         "AAR 特別擅長 data/model-specific tricks。",
         ACC_WARN),
        ("2", "跨 model scale",
         "小模型上發現的 idea 不一定在大模型上適用；反之亦然。涉及 RL 與 in-context learning 的方向在小模型上多半失敗（能力限制），但可能在更強的模型上有效。",
         ACC_WARN),
        ("3", "Production scale",
         "模糊獎勵（硬體效率、infrastructure 相容性）超出單一 task metric。",
         ACC_BAD),
    ]
    sy, sh, gap = 22.0, 12.0, 1.5
    for num, name, desc, color in scales:
        ix, iy, iw, ih = panel(sl, 4, sy, 92, sh, stripe=color)
        text(sl, num, ix, iy, 5, ih,
             size=22, bold=True, color=color, font='mono',
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, name, ix + 6, iy + 0.5, 20, ih - 1,
             size=T_BODY + 1, bold=True, color=TEXT_PRIM,
             anchor=MSO_ANCHOR.MIDDLE)
        text(sl, desc, ix + 27, iy + 1.5, iw - 28, ih - 3,
             size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.35)
        sy += sh + gap

    ix, iy, iw, ih = panel(sl, 4, 64, 92, 28, stripe=ACC_BAD, fill=PANEL_BAD)
    text(sl, "OOD TEST 的重要警示", ix, iy, iw, 5,
         size=T_BODY_SM, color=TEXT_MUTED, font='mono')
    text(sl, "OOD test 抓不出 data/model-specific tricks", ix, iy + 5, iw, 6,
         size=T_H2 - 2, bold=True, color=ACC_BAD)
    text_lines(sl, [
        ('"AAR is particularly good at discovering data- and model-specific tricks. However, unlike traditional shortcut learning in ML, these cannot be simply detected by out-of-distribution tests: on math and coding, high-PGR ideas that exploit dataset patterns successfully generalize to our OOD test data."',
         {'size': T_BODY_SM - 1, 'color': TEXT_PRIM,
          'italic': True, 'line_spacing': 1.4}),
        ("→ 未來工作應在 hill-climbing 階段就用多個 domain / dataset，並在完全沒見過的新 dataset 上做最終測試。",
         {'size': T_BODY_SM, 'color': ACC_GOOD,
          'space_before': 5, 'bold': True, 'line_spacing': 1.4}),
    ], ix, iy + 13, iw, ih - 15)

    ax_footer(sl, "F3")
    set_notes(sl, """【F3｜3 種尺度 + OOD 盲點】論文 Sec 7。深化主 deck Slide 29 open question 2。

跨 dataset / 跨 model scale / production 三個尺度。
OOD test 的關鍵警示：抓不出 data/model-specific tricks。""")


def slide_F4():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "Sec 7 'Richer logs of science' + 'Alien science'",
            deck_tie="擴展 Slide 29 open question 4")
    h1(sl, "F4 · Richer logs of science · Alien science · Legibility training",
       y=7.5, h=10, size=22)

    ix, iy, iw, ih = panel(sl, 4, 22, 44, 65, stripe=ACC_GOOD, fill=PANEL_GOOD)
    text(sl, "RICHER LOGS OF SCIENCE", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "一個 AAR 天然產出的科學新資產", ix, iy + 4, iw, 6,
         size=T_H2 - 4, bold=True, color=ACC_GOOD, line_spacing=1.2)
    text_lines(sl, [
        ("傳統科學論文只發表「最終成功的結果」，路上試過但失敗的 promising idea 不會被記錄。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM, 'line_spacing': 1.4}),
        ("AAR 天然產生這些 logs：每個 negative result、每個 dead-end hyperparameter、每個「應該有效但沒有」都被預設記下來。",
         {'size': T_BODY_SM, 'color': ACC_GOOD,
          'space_before': 6, 'line_spacing': 1.4}),
        ("兩種用途：",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 8, 'bold': True}),
        ("1. 未來 AAR 的訓練資料",
         {'size': T_BODY_SM, 'color': TEXT_SEC,
          'space_before': 2, 'line_spacing': 1.3}),
        ("2. 可搜尋的紀錄，省下下個研究者重複犯同樣失敗",
         {'size': T_BODY_SM, 'color': TEXT_SEC,
          'space_before': 2, 'line_spacing': 1.3}),
    ], ix, iy + 12, iw, ih - 14)

    ix, iy, iw, ih = panel(sl, 52, 22, 44, 65, stripe=ACC_WARN)
    text(sl, "ALIEN SCIENCE", ix, iy, iw, 4,
         size=T_CAPTION, color=TEXT_MUTED, font='mono')
    text(sl, "兩面性 + Legibility 緩解方向", ix, iy + 4, iw, 6,
         size=T_H2 - 4, bold=True, color=ACC_WARN, line_spacing=1.2)
    text_lines(sl, [
        ("🟢 樂觀面",
         {'size': T_BODY_SM, 'bold': True, 'color': ACC_GOOD}),
        ("AAR 可發現人類想不到的 idea（如 Overlap Density），拓寬科學的探索空間。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 2, 'line_spacing': 1.35}),
        ("🔴 風險面",
         {'size': T_BODY_SM, 'bold': True, 'color': ACC_BAD, 'space_before': 6}),
        ("如果只被優化 outcome reward，最終會出現難以驗證的 idea。",
         {'size': T_BODY_SM, 'color': TEXT_PRIM,
          'space_before': 2, 'line_spacing': 1.35}),
        ("目前狀況",
         {'size': T_BODY_SM, 'bold': True, 'color': TEXT_PRIM, 'space_before': 6}),
        ("AAR 的 idea 仍是 understandable — 利用 training dynamics、consistency、model output/internals、information theory、probabilistic theory。",
         {'size': T_BODY_SM - 1, 'color': TEXT_SEC,
          'space_before': 2, 'line_spacing': 1.3}),
        ("→ 緩解：對 AAR 加入 legibility training — 不只 reward outcome，也 reward「可讀性 / 可驗證性」。",
         {'size': T_BODY_SM, 'color': ACC_GOOD_GLOW,
          'space_before': 5, 'bold': True, 'line_spacing': 1.35}),
    ], ix, iy + 12, iw, ih - 14)

    ax_footer(sl, "F4")
    set_notes(sl, """【F4｜Richer logs + Alien science + Legibility】論文 Sec 7。擴展主 deck Slide 29 open question 4。

兩個概念：(1) AAR 天然產出失敗 log，是科學新資產；(2) Alien science 的兩面性 → legibility training 是緩解方向。""")


def slide_F5():
    sl = add_slide(BG_BASE)
    ax_meta(sl, "自整理（非論文原文）", deck_tie="—")
    h1(sl, "F5 · 論文未明說的 caveats（整理者觀察）",
       y=7.5, h=10, size=24)

    # Watermark
    text(sl, "INTEGRATOR'S NOTE · NOT FROM PAPER",
         4, 17, 92, 4, size=T_BODY_SM, bold=True, color=ACC_WARN,
         font='mono', align=PP_ALIGN.CENTER)
    rect(sl, 4, 21, 92, 0.3, fill=ACC_WARN)

    text(sl, "⚠ 本節為整理者觀察。標註的目的是讓 DS 同事在引用論文數字時有風險意識。",
         4, 23, 92, 5, size=T_BODY_SM, color=TEXT_SEC, italic=True,
         align=PP_ALIGN.CENTER)

    caveats = [
        ("Variance / CI 未報告",
         "9 runs；PGR 0.97 無 CI / SD — 視為最佳單次執行，非期望均值。"),
        ("與 Burns et al. 2023 W2SG 原始論文的對照只有一句",
         "論文 Sec 1 提到「考慮了更廣的方法集合」，沒有 methodological 對照表。"),
        ("三類 baseline 的具體 PGR 沒分開列",
         "論文只說「最佳 PGR 0.23」，沒有 per-method 的對照。"),
        ("Production transfer 細節有限",
         "Sonnet 4.0 + 生產 infrastructure 的具體配置（資料量、batch size、step 數）沒公開。"),
        ("「Unlimited submissions」hack 影響哪些 metric 沒有完整分析",
         "作者表示「實際 submission 限制不會阻止 hack」，但沒給出量化曲線。"),
        ("PGR 公式中 P_strong_ceiling 的計算協定",
         "論文用 ground-truth-supervised student 當天花板，但訓練該 student 的細節（資料量、loss、收斂判定）沒展開。"),
    ]
    sy, sh, gap = 25.0, 11.0, 0.5   # 25+6×11+5×0.5=93.5%; body_h=3.1 fits iy+7.3≤7.574
    for head, body in caveats:
        ix, iy, iw, ih = panel(sl, 4, sy, 92, sh, stripe=ACC_WARN, fill=PANEL_2)
        text(sl, head, ix, iy + 0.2, iw, 4,
             size=T_BODY_SM, bold=True, color=TEXT_PRIM)
        text(sl, body, ix, iy + 4.2, iw, sh - 7.9,
             size=T_BODY_SM - 1, color=TEXT_SEC, line_spacing=1.3)
        sy += sh + gap

    ax_footer(sl, "F5")
    set_notes(sl, """【F5｜整理者觀察 caveats】非論文原文。

引用本節時務必標明「整理者觀察」，不要當論文結論引用。
目的：讓 DS 同事在引用論文數字時有風險意識。""")


# ════════════════════════════════════════════════════════════════════════
# CLOSING
# ════════════════════════════════════════════════════════════════════════
def closing():
    sl = add_slide(BG_DOSSIER)
    dossier_frame(sl, "END OF APPENDIX",
                  "REFERENCE COMPLETE // RETURN TO MAIN DECK FOR Q&A")
    h1(sl, "附錄使用建議", y=10, h=10, size=32)
    text(sl, "Q&A 應對節奏 · 根據問題類型快速調出對應主題",
         4, 19, 92, 6, size=T_BODY, color=TEXT_SEC, italic=True)

    mappings = [
        ("被問「實驗用什麼模型 / 資料」", "→ 翻 A1–A3", ACC_DATA_BLUE),
        ("被問「他們具體做了什麼 hack」", "→ 翻 D1–D4", ACC_BAD),
        ("被問「這方法能不能搬到我們的場景」", "→ 翻 E1–E3 與 F3", ACC_WARN),
        ("被問「這篇論文的科學限制是什麼」", "→ 翻 F4–F5", ACC_GOOD),
    ]
    sy, sh, gap = 28.0, 12.0, 2.0
    for q, route, color in mappings:
        ix, iy, iw, ih = panel(sl, 6, sy, 88, sh, stripe=color)
        text(sl, q, ix, iy + 1, 50, ih - 2,
             size=T_BODY + 1, color=TEXT_PRIM, anchor=MSO_ANCHOR.MIDDLE)
        text(sl, route, ix + 52, iy + 1, iw - 52, ih - 2,
             size=T_BODY + 1, bold=True, color=color,
             anchor=MSO_ANCHOR.MIDDLE, font='mono')
        sy += sh + gap

    text(sl, "End of Appendix.", 4, 86, 92, 5,
         size=T_BODY, color=TEXT_MUTED, italic=True, align=PP_ALIGN.CENTER,
         font='mono')

    ax_footer(sl, "END")
    set_notes(sl, """【結語｜附錄使用建議】

附錄可在主 deck 第 31 張結束、開放 Q&A 之前選擇性穿插展示，或全數放在「Backup Slides」區。

Q&A 應對節奏（4 種典型問題對應 4 個主題群）。

視覺風格沿用 vis_style.md；附錄頁右下角加 'APPENDIX · A{N}' 標記，與主 deck 區隔。""")


# ════════════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════════════
def main():
    builders = [
        cover,
        divider_A, slide_A1, slide_A2, slide_A3, slide_A4, slide_A5,
        divider_B, slide_B1, slide_B2, slide_B3, slide_B4,
        divider_C, slide_C1, slide_C2, slide_C3, slide_C4, slide_C5,
        divider_D, slide_D1, slide_D2, slide_D3, slide_D4,
        divider_E, slide_E1, slide_E2, slide_E3,
        divider_F, slide_F1, slide_F2, slide_F3, slide_F4, slide_F5,
        closing,
    ]
    assert len(builders) == TOTAL, f"expected {TOTAL} slides, got {len(builders)}"
    for b in builders:
        b()
    prs.save(OUT)
    print(f"{len(prs.slides)} slides, "
          f"{prs.slide_width.inches:.2f}\" x {prs.slide_height.inches:.2f}\"")
    print(f"saved: {OUT}")


if __name__ == "__main__":
    main()
