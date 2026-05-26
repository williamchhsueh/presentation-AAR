"""
gen_fig04_ppt.py — Generate two PPT-optimized versions of the AAR setup
overview diagram with larger text.

Usage:
    poetry run python code/gen_fig04_ppt.py

Outputs:
    figure/paper_fig04_AAR_setup_overview_v4.png  (font scale ×1.35 — "medium large")
    figure/paper_fig04_AAR_setup_overview_v5.png  (font scale ×1.70 — "max legibility")
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# ---------------------------------------------------------------------------
# Color tokens  (vis_style.md §4)
# ---------------------------------------------------------------------------
BG_BASE        = "#081010"
PANEL          = "#101818"
PANEL_2        = "#181820"
PANEL_BAD      = "#1A0E10"
STROKE         = "#283038"
STROKE_HUD     = "#3A4A55"
TEXT_PRIMARY   = "#F8F8F8"
TEXT_SECONDARY = "#B8C0C4"
TEXT_MUTED     = "#7A8488"
ACCENT_GOOD    = "#7CE38B"
ACCENT_BAD     = "#C73838"
ROLE_DS        = "#E36AAE"


def build_diagram(version: int, font_scale: float) -> None:
    """Render the AAR setup overview at the given font_scale and save as vN."""

    S = dict(
        sz_title_lg   = round(16 * font_scale),
        sz_title_md   = round(14 * font_scale),
        sz_title_sm   = round(13 * font_scale),
        sz_sub_lg     = round(11 * font_scale),
        sz_sub_md     = round(10 * font_scale),
        sz_label      = round(10 * font_scale),
        sz_dots       = round(14 * font_scale),
        # borders / arrows unchanged
        lw_box_hi     = 2.5,
        lw_box_md     = 2.0,
        lw_dash_outer = 2.8,
        lw_dash_inner = 2.4,
        lw_hud        = 2.0,
        lw_glow       = 8.0,
        arr_lw        = 1.8,
        arr_hw        = 1.0,
        arr_hl        = 0.8,
        arr_lw_side   = 1.8,
        arr_hw_side   = 0.9,
        arr_hl_side   = 0.7,
    )

    plt.rcParams.update({
        "font.family":      "sans-serif",
        "font.sans-serif":  ["Inter", "Helvetica Neue", "Liberation Sans",
                             "DejaVu Sans", "Arial"],
        "axes.facecolor":   BG_BASE,
        "figure.facecolor": BG_BASE,
    })

    DPI = 150
    FIG_W, FIG_H = 1920 / DPI, 1200 / DPI   # taller canvas: 1920×1200
    W, H = 128, 80

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")

    # --- helpers -----------------------------------------------------------

    def rrect(x, y, w, h, fc, ec, lw=1.0, radius=1.2,
              alpha=1.0, ls="-", zorder=2):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            facecolor=fc, edgecolor=ec,
            linewidth=lw, alpha=alpha, linestyle=ls,
            zorder=zorder,
        )
        ax.add_patch(patch)

    def glow(x, y, w, h, color, layers=3, spread=0.65,
             base_alpha=0.18, base_lw=None, radius=1.2):
        if base_lw is None:
            base_lw = S["lw_glow"]
        for i in range(layers, 0, -1):
            e = i * spread
            rrect(x - e, y - e, w + 2*e, h + 2*e,
                  fc="none", ec=color, lw=base_lw / i,
                  radius=radius + e, alpha=base_alpha / i, zorder=1)

    def dashed(x, y, w, h, color, lw=1.0, radius=1.5, fc="none"):
        rrect(x, y, w, h, fc=fc, ec=color, lw=lw,
              radius=radius, ls=(0, (6, 4)), zorder=2)

    def txt(x, y, s, size=9, color=TEXT_PRIMARY, ha="center", va="center",
            weight="normal", style="normal", rotation=0, zorder=8):
        ax.text(x, y, s, fontsize=size, color=color,
                ha=ha, va=va, fontweight=weight, fontstyle=style,
                rotation=rotation, rotation_mode="anchor", zorder=zorder)

    def arrow(x1, y1, x2, y2, color=TEXT_SECONDARY,
              lw=None, hw=None, hl=None, zorder=6, style="arc3,rad=0"):
        if lw is None: lw = S["arr_lw"]
        if hw is None: hw = S["arr_hw"]
        if hl is None: hl = S["arr_hl"]
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            xycoords="data", textcoords="data",
            arrowprops=dict(
                arrowstyle=f"-|>,head_width={hw},head_length={hl}",
                color=color, lw=lw, connectionstyle=style,
            ),
            zorder=zorder,
        )

    def bidir(x, y1, y2, color=STROKE_HUD, lw=None, hw=None, hl=None, zorder=6):
        if lw is None: lw = S["arr_lw"]
        if hw is None: hw = S["arr_hw"]
        if hl is None: hl = S["arr_hl"]
        ax.annotate(
            "", xy=(x, y2), xytext=(x, y1),
            arrowprops=dict(
                arrowstyle=f"<|-|>,head_width={hw},head_length={hl}",
                color=color, lw=lw,
            ),
            zorder=zorder,
        )

    def hud_corners(x, y, w, h, leg=3.0, lw=None, color=STROKE_HUD):
        if lw is None: lw = S["lw_hud"]
        segs = [
            [(x, y+leg), (x, y), (x+leg, y)],
            [(x+w-leg, y), (x+w, y), (x+w, y+leg)],
            [(x, y+h-leg), (x, y+h), (x+leg, y+h)],
            [(x+w-leg, y+h), (x+w, y+h), (x+w, y+h-leg)],
        ]
        for pts in segs:
            ax.plot([p[0] for p in pts], [p[1] for p in pts],
                    color=color, lw=lw, solid_capstyle="butt", zorder=10)

    # --- layout constants (unchanged geometry) -----------------------------
    DX, DY, DW, DH = 26, 1.5, 76, 7.5
    SX, SY, SW, SH = 6.5, 16, 115, 31.5    # SY→16: gap below Dashboard = 7
    AAR_Y,  AAR_H  = 19.0, 12.5             # AAR_Y→19: keeps 3-unit offset from SY
    AAR_W          = 30
    AAR_XS         = [9.5, 47, 84.5]
    HLP_Y,  HLP_H  = 33.5, 10.5             # HLP_Y→33.5: same relative shift
    HLP_W          = 30
    IX, IY, IW, IH = 6.5, 53.5, 115, 14.5  # IY→53.5: sandbox bottom=47.5, gap=6
    FRX, FRY, FRW, FRH = 9.5,  56.5, 53, 9  # FRY→56.5: keeps 3-unit offset from IY
    CDX, CDY, CDW, CDH = 64.0, 56.5, 53, 9  # CDY→56.5: same
    EX, EY, EW, EH  = 24, 69.5, 80, 7.5     # EY→69.5: infra bottom=68, gap=1.5
    LX    = 3.5
    L_TOP = SY + 2.5
    L_BOT = EY + EH / 2

    ax.set_facecolor(BG_BASE)

    # Shared-infra container
    dashed(IX, IY, IW, IH, color=STROKE_HUD, lw=S["lw_dash_inner"], radius=1.5, fc=PANEL)
    ax.patches[-1].set_alpha(0.55)
    txt(IX + 4, IY + 1.2,
        "Shared persistent infra  ·  outside sandbox",
        size=S["sz_label"], color=TEXT_SECONDARY, ha="left", style="italic")

    # Forum
    rrect(FRX, FRY, FRW, FRH, fc=PANEL, ec=ACCENT_GOOD,
          lw=S["lw_box_md"], radius=1.1, zorder=3)
    txt(FRX + FRW/2, FRY + 3.0, "Forum",
        size=S["sz_title_sm"], weight="semibold", color=ACCENT_GOOD)
    txt(FRX + FRW/2, FRY + 6.5, "share & read findings",
        size=S["sz_sub_md"], color=TEXT_SECONDARY)

    # Codebase storage
    rrect(CDX, CDY, CDW, CDH, fc=PANEL, ec=ACCENT_GOOD,
          lw=S["lw_box_md"], radius=1.1, zorder=3)
    txt(CDX + CDW/2, CDY + 3.0, "Codebase storage",
        size=S["sz_title_sm"], weight="semibold", color=ACCENT_GOOD)
    txt(CDX + CDW/2, CDY + 6.5, "upload / download snaps",
        size=S["sz_sub_md"], color=TEXT_SECONDARY)

    # Sandbox container
    dashed(SX, SY, SW, SH, color=STROKE_HUD, lw=S["lw_dash_outer"], radius=1.8)
    txt(SX + 4, SY + 1.2,
        "Parallel AAR agents  ·  independent sandboxes",
        size=S["sz_label"], color=TEXT_SECONDARY, ha="left", style="italic")

    # Helper-function boxes
    for xi in AAR_XS:
        cx = xi + HLP_W / 2
        rrect(xi, HLP_Y, HLP_W, HLP_H, fc=PANEL, ec=ACCENT_GOOD,
              lw=S["lw_box_md"], radius=1.1, zorder=3)
        txt(cx, HLP_Y + 3.2, "Helper functions",
            size=S["sz_title_sm"], weight="semibold", color=ACCENT_GOOD)
        txt(cx, HLP_Y + 7.0, "train / infer / baselines",
            size=S["sz_sub_md"], color=TEXT_SECONDARY)

    # AAR agent boxes
    NAMES = ["AAR 1", "AAR 2", "AAR N"]
    for xi, name in zip(AAR_XS, NAMES):
        glow(xi, AAR_Y, AAR_W, AAR_H, ROLE_DS, layers=3, spread=0.55, base_alpha=0.16)
        rrect(xi, AAR_Y, AAR_W, AAR_H, fc=PANEL_2, ec=ROLE_DS,
              lw=S["lw_box_md"], radius=1.2, zorder=3)
        cx = xi + AAR_W / 2
        txt(cx, AAR_Y + 2.5, name,
            size=S["sz_title_md"], weight="semibold", color=ROLE_DS)
        txt(cx, AAR_Y + 5.2, "propose ideas",   size=S["sz_sub_md"], color=TEXT_SECONDARY)
        txt(cx, AAR_Y + 7.4, "run experiments", size=S["sz_sub_md"], color=TEXT_SECONDARY)
        txt(cx, AAR_Y + 9.6, "analyze results", size=S["sz_sub_md"], color=TEXT_SECONDARY)

    AAR2_R = AAR_XS[1] + AAR_W
    AARN_L = AAR_XS[2]
    txt((AAR2_R + AARN_L) / 2, AAR_Y + AAR_H / 2, "· · ·",
        size=S["sz_dots"], color=TEXT_MUTED)

    # Dashboard
    glow(DX, DY, DW, DH, ACCENT_GOOD, layers=2, spread=0.5, base_alpha=0.12)
    rrect(DX, DY, DW, DH, fc=PANEL, ec=ACCENT_GOOD,
          lw=S["lw_box_hi"], radius=1.2, zorder=4)
    txt(DX + DW/2, DY + 2.8, "Dashboard",
        size=S["sz_title_lg"], weight="semibold")
    txt(DX + DW/2, DY + 5.5, "Launch & monitor team",
        size=S["sz_sub_lg"], color=TEXT_SECONDARY)

    # Remote evaluation API
    glow(EX, EY, EW, EH, ACCENT_BAD, layers=2, spread=0.5, base_alpha=0.16)
    rrect(EX, EY, EW, EH, fc=PANEL_BAD, ec=ACCENT_BAD,
          lw=S["lw_box_hi"], radius=1.2, zorder=4)
    txt(EX + EW/2, EY + 2.8, "Remote evaluation API",
        size=S["sz_title_lg"], weight="semibold", color=ACCENT_BAD)
    txt(EX + EW/2, EY + 5.5, "submit preds → PGR",
        size=S["sz_sub_lg"], color=TEXT_SECONDARY)

    # Arrows
    DASH_BX = DX + DW / 2
    for xi in AAR_XS:
        arrow(DASH_BX, DY + DH, xi + AAR_W / 2, SY, color=TEXT_SECONDARY)
    for xi in AAR_XS:
        bidir(xi + HLP_W / 2, SY + SH, IY, color=STROKE_HUD)

    lw_s = S["arr_lw_side"]
    ax.plot([LX, LX], [L_TOP, L_BOT], color=STROKE_HUD, lw=lw_s, zorder=5)
    ax.plot([LX, SX], [L_TOP, L_TOP], color=STROKE_HUD, lw=lw_s, zorder=5)
    ax.plot([LX, EX], [L_BOT, L_BOT], color=STROKE_HUD, lw=lw_s, zorder=5)
    arrow(LX, L_BOT, EX + 0.1, L_BOT, color=STROKE_HUD,
          lw=lw_s, hw=S["arr_hw_side"], hl=S["arr_hl_side"])

    ax.text(LX - 1.6, (L_TOP + L_BOT) / 2, "submit / score",
            fontsize=S["sz_label"], color=TEXT_MUTED,
            ha="center", va="center", rotation=90, rotation_mode="anchor", zorder=8)

    # HUD frame
    hud_corners(1.0, 1.0, W - 2, H - 2, leg=3.5)

    # Save
    base = Path(__file__).parent.parent / "figure" / f"paper_fig04_AAR_setup_overview_v{version}"
    fig.savefig(base.with_suffix(".png"), dpi=DPI, bbox_inches="tight", pad_inches=0, facecolor=BG_BASE)
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight", pad_inches=0, facecolor=BG_BASE)
    print(f"Saved → {base}.{{png,svg}}  (font_scale={font_scale}×)")
    plt.close(fig)


if __name__ == "__main__":
    build_diagram(version=4, font_scale=1.35)   # medium-large
    build_diagram(version=5, font_scale=1.70)   # max legibility
