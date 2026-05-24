#!/usr/bin/env python3
"""
patch_slides.py - Rebuild image-only slides 1, 18, 22, 26 in v4.1.pptx as editable.

Each target slide contained a single full-slide raster PNG with no editable elements.
This script clears those slides in-place and rebuilds them using the same helper
functions and design tokens as build_deck.py.

Mapping to build_deck.py equivalents:
  v4.1 slide 1  (index 0)  → slide_01() content
  v4.1 slide 18 (index 17) → slide_13() content
  v4.1 slide 22 (index 21) → slide_15() content
  v4.1 slide 26 (index 25) → slide_17() content

Usage: poetry run python code/patch_slides.py
Output: ppt/AAR_Paper_Sharing_v4.2.pptx
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from pptx.oxml.ns import qn

import build_deck as bd
from build_deck import (
    BG_BASE, BG_DOSSIER,
    PANEL, PANEL_BAD,
    STROKE, STROKE_HUD,
    TEXT_PRIM, TEXT_SEC, TEXT_MUTED,
    ACC_GOOD, ACC_GOOD_GLOW, ACC_WARN, ACC_BAD,
    PP_ALIGN, MSO_ANCHOR,
    set_bg, set_notes,
    text, text_lines, rect,
    panel, badge_role, dossier_frame, footer, fig_embed,
    h1, _fig_half,
    T_H2, T_BODY_SM, T_CAPTION,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE_DIR, "ppt", "AAR_Paper_Sharing_v4.1.pptx")
OUT = os.path.join(BASE_DIR, "ppt", "AAR_Paper_Sharing_v4.2.pptx")

_SHAPE_TAGS = ("p:sp", "p:pic", "p:grpSp", "p:graphicFrame", "p:cxnSp")


def clear_slide(slide):
    sp_tree = slide.shapes._spTree
    for tag in _SHAPE_TAGS:
        for elem in list(sp_tree.findall(qn(tag))):
            sp_tree.remove(elem)


# ── Slide 1 (index 0): Opening comparison ─────────────────────────────────
def rebuild_01(sl):
    set_bg(sl, BG_BASE)
    ix, iy, iw, ih = panel(sl, 10, 34, 36, 28, border=STROKE)
    text_lines(sl, [
        ("2 Human Researchers × 7 Days",
         {"size": T_H2, "color": TEXT_SEC, "align": PP_ALIGN.CENTER}),
        ("= PGR 0.23",
         {"size": T_H2, "bold": True, "color": TEXT_PRIM,
          "align": PP_ALIGN.CENTER, "space_before": 12}),
    ], ix, iy, iw, ih, anchor=MSO_ANCHOR.MIDDLE)
    ix, iy, iw, ih = panel(sl, 54, 34, 36, 28, border=ACC_GOOD)
    text_lines(sl, [
        ("9 Autonomous AI Agents × 5 Days",
         {"size": T_H2, "color": TEXT_SEC, "align": PP_ALIGN.CENTER}),
        ([("= PGR ", {"color": TEXT_PRIM}), ("0.97", {"color": ACC_GOOD_GLOW})],
         {"size": T_H2, "bold": True, "align": PP_ALIGN.CENTER, "space_before": 12}),
    ], ix, iy, iw, ih, anchor=MSO_ANCHOR.MIDDLE)
    footer(sl, page_no=None)
    set_notes(sl, """【Slide 01｜冷開場：7 天 vs 5 天】幕別：第一幕 超大型巨人　主導：A 戲劇張力

Core：全黑投影片，正中央兩行白字。停 3 秒、無聲，再開口。

Deeper（🔵DS）：兩個數字都來自論文 baseline。人類部分是兩位 Anthropic 研究員依 W2SG 任務做的 hill-climbing；AI 部分是 9 個 AAR 並行運行的最佳結果。

Wider（🟢PM）：這頁的訊息不是「AI 比人強」，而是「成本結構正在改寫」——研究這件事的單位成本，從『人月』變成『美金小時』。

停頓：3 秒""")


# ── Slide 18 (index 17): PGR chart — same content as build_deck slide_13 ──
def rebuild_18(sl):
    set_bg(sl, BG_BASE)
    h1(sl, "The AAR formation rapidly approaches the theoretical ceiling.")
    fig_embed(sl, 4, 25, 92, 56, "paper_fig01_PGR_vs_hillclimbing_hours.png",
              caption="Figure 1 — 9 個 AAR 的 PGR 時序：0.23 → 0.97（前 2 天最陡）。")
    ix, iy, iw, ih = panel(sl, 6, 27, 32, 8, fill=PANEL, tick=False)
    text(sl, [("Human Benchmark (7 Days):  ", {"color": TEXT_SEC}),
              ("PGR 0.23", {"color": TEXT_SEC, "bold": True})],
         ix, iy, iw, ih, size=T_BODY_SM, anchor=MSO_ANCHOR.MIDDLE)
    rect(sl, 62, 27, 32, 8, fill=PANEL, line_color=ACC_GOOD, line_w=1.0)
    text(sl, [("AAR Benchmark (5 Days):  ", {"color": TEXT_PRIM}),
              ("PGR 0.97", {"color": ACC_GOOD_GLOW, "bold": True})],
         63, 27, 30, 8, size=T_BODY_SM, anchor=MSO_ANCHOR.MIDDLE)
    badge_role(sl, 4, 82.5, "PM")
    text(sl, "In 800 hours the AAR compressed months of human trial-and-error into "
             "5 days — discovering new variants of Contrastive Consistency Search "
             "and EM Posterior methods that humans had not hypothesized.",
         12, 82.6, 84, 10, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)
    footer(sl, 13)
    set_notes(sl, """【Slide 13｜第一翻：勝利】幕別：第四幕 艾連覺醒　主導：A 戲劇張力

Core：9 個 AAR，5 天，$18,000，從 0.23 爬到 0.97。講完直接翻 Slide 14，不停頓。

Deeper（🔵DS）：$18,000 是 inference 成本估算，論文有揭露。爬升曲線顯示前 2 天最陡。

Wider（🟢PM）：一個月研究預算 $18,000，比僱用一位 alignment researcher 一週還便宜。

停頓：0 秒（直接翻下一頁）""")


# ── Slide 22 (index 21): Transfer results — same content as build_deck slide_15 ─
def rebuild_22(sl):
    set_bg(sl, BG_BASE)
    h1(sl, "We built a student that solves the test, but cannot trust its work.")
    fig_embed(sl, 4, 25, 92, 39, "paper_fig09_AAR_ideas_transfer.png",
              caption="Figure 9 — AAR 方法跨 dataset 的泛化結果矩陣。")
    stat3 = [
        ("0.97", "Chat  ✓",           ACC_GOOD, ACC_GOOD, PANEL),
        ("0.94", "Math  ✓",           ACC_GOOD, ACC_GOOD, PANEL),
        ("0.47", "Code — The Anomaly", ACC_BAD,  ACC_BAD,  PANEL_BAD),
    ]
    cw, gap, x = 29.3, 2.05, 4.0
    for val, lab, stripe, vc, fill in stat3:
        ix, iy, iw, ih = panel(sl, x, 65, cw, 16, stripe=stripe, fill=fill)
        text(sl, val, ix, iy - 0.5, iw, 9, size=42, bold=True, color=vc,
             align=PP_ALIGN.CENTER)
        text(sl, lab, ix, iy + ih - 4, iw, 4, size=T_BODY_SM, color=TEXT_SEC,
             align=PP_ALIGN.CENTER, font="mono")
        x += cw + gap
    rect(sl, 4, 83, 92, 10.5, fill=PANEL_BAD, line_color=ACC_BAD, line_w=1.0)
    text(sl, "The 0.47 Code failure proves the AAR found a solution that did not "
             "rely on weak labels at all. By executing code to get the answer it "
             "solved the benchmark but violated the entire premise of W2SG — it "
             "succeeded at the metric, but failed the alignment goal.",
         6, 84, 88, 9, size=T_BODY_SM, color=TEXT_SEC, line_spacing=1.3)
    footer(sl, 15)
    set_notes(sl, """【Slide 15｜第三翻：證據】幕別：第四幕 艾連覺醒　主導：A + B

Core：Chat 0.97 ✓、Math 0.94 ✓、Code 0.47 ⚠️。「AAR 成功了，但不是用我們想要的方式——在 Code 任務上它繞過了弱監督，直接預測 label distribution。」停 8 秒，然後直接切金句卡。

Deeper（🔵DS）：Code 0.47 不是模型能力問題——AAR 找到「不依賴 weak labels」的解法，這在 W2SG 設定下等於作弊。論文用 fig09 顯示泛化矩陣。

Wider（🟢PM）：0.47 比 0.97 是「失敗」，但對部署更重要的問題是：你能不能事前判斷哪些任務會出現這種繞道？目前還不能。

停頓：8 秒（停完直接切金句卡 4）""")


# ── Slide 26 (index 25): Scalable Oversight Dilemma — same as build_deck slide_17 ─
def rebuild_26(sl):
    set_bg(sl, BG_DOSSIER)
    dossier_frame(sl, "SCALABLE OVERSIGHT", "STATUS: CRITICAL // RISK ASSESSMENT: HIGH")
    h1(sl, "The Scalable Oversight Dilemma: Control versus Creativity.",
       x=6, y=11, w=88, h=10, size=26)
    cols = [
        (6, "Prescriptive Scaffolding", STROKE_HUD, "L",
         "Fixed workflow loops — Propose → Plan → Code → Test → Analyze.",
         [("High control, highly auditable, predictable. ", {"color": TEXT_SEC}),
          ("BUT severely limits AAR creativity → lower performance.", {"color": TEXT_SEC})]),
        (52, "Autonomous Scaffolding", ACC_WARN, "R",
         "Free-form decision making — the AAR decides its own next step.",
         [("Acts like a true researcher; achieves ", {"color": TEXT_SEC}),
          ("SOTA performance", {"color": ACC_GOOD, "bold": True}),
          (". BUT high risk of ", {"color": TEXT_SEC}),
          ("reward hacking", {"color": ACC_BAD, "bold": True}),
          (", nearly impossible to verify beforehand.", {"color": TEXT_SEC})]),
    ]
    for cx, title, stripe, side, mech, trade in cols:
        ix, iy, iw, ih = panel(sl, cx, 25, 42, 58, stripe=stripe)
        _fig_half(sl, ix, iy, iw, ih * 0.34,
                  "paper_fig10_scaffolding_schematic.png", side)
        cy = iy + ih * 0.34 + 2.5
        text(sl, title, ix, cy, iw, 5, size=T_H2 - 2, bold=True, color=TEXT_PRIM)
        text(sl, "MECHANISM", ix, cy + 5.6, iw, 3.5, size=T_CAPTION,
             color=TEXT_MUTED, font="mono")
        text(sl, mech, ix, cy + 8.8, iw, 9, size=T_BODY_SM, color=TEXT_SEC,
             line_spacing=1.25)
        text(sl, "THE TRADE-OFF", ix, cy + 18, iw, 3.5, size=T_CAPTION,
             color=TEXT_MUTED, font="mono")
        text(sl, trade, ix, cy + 21.2, iw, 14, size=T_BODY_SM, line_spacing=1.25)
    text(sl, "There is no correct answer, only a strategic trade-off. We chose "
             "Autonomous to see the true ceiling — accepting the risk of Alien Science.",
         6, 85, 88, 6, size=T_BODY_SM, italic=True, color=TEXT_SEC,
         align=PP_ALIGN.CENTER)
    footer(sl, 17)
    set_notes(sl, """【Slide 17｜瓶頸搬家了】幕別：第五幕 阿爾敏的價值　主導：C PM 行動 + B 打底

Core：提出想法、跑實驗，已經被自動化了（$22／AAR-hour）；守不住的下一道牆，是設計一個 AAR 鑽不動的 eval。

Deeper（🔵DS）：論文 Sec 1——unlimited submission 讓 test set 實質變成 validation set。
Deeper（🟠SE）：四個 reward hacking case 全是系統層級漏洞。eval 要當 attack surface 來設計。

Wider（🟢PM）：「The key bottleneck for alignment research is moving from proposing and executing ideas to designing evals.」

停頓：3 秒""")


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    prs = Presentation(SRC)
    targets = {
        0:  (rebuild_01, "Slide 1  — opening comparison (was image1.png)"),
        17: (rebuild_18, "Slide 18 — PGR chart          (was image8.png)"),
        21: (rebuild_22, "Slide 22 — transfer results   (was image11.png)"),
        25: (rebuild_26, "Slide 26 — scalable oversight (was image13.png)"),
    }
    for idx, (fn, label) in sorted(targets.items()):
        sl = prs.slides[idx]
        clear_slide(sl)
        fn(sl)
        print(f"  rebuilt: {label}")
    prs.save(OUT)
    print(f"\nSaved: {OUT}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()
