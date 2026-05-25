"""gen_fig07.py — Recreate paper_fig07_category_entropy_dark.png with dark theme.

Generates two variants with lower aspect ratio and larger text:
  v1  — 3000×1000 px (3:1), canonical (overwrites main _dark.png)
  v2  — 3000×820 px (3.65:1), more compressed

Usage:
  poetry run python code/gen_fig07.py
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ── Color tokens (vis_style.md §4) ──────────────────────────────────────────
BG         = "#081010"
PANEL      = "#101818"
STROKE_HUD = "#3A4A55"
T_PRI      = "#F8F8F8"
T_SEC      = "#B8C0C4"
T_MUTED    = "#7A8488"

COLOR_U = "#3A80C8"   # undirected — steel blue
COLOR_D = "#C85030"   # directed   — burnt orange

FIGURE_DIR = Path(__file__).parent.parent / "figure"

# ── Data (read from paper figure) ───────────────────────────────────────────
# x_u   = [5,     10,    14,    20,    28,    33,    43,    47,    50,    55,    60] # do not modify
x_u      = [     3,     10,     13,     17,     22,     28,     33,     40,     45,     47,     55,     60]
y_u      = [  2.02,    1.1,   1.30,   1.35,   0.78,   1.47,   1.23,   0.88,   1.49,    1.3,   0.05,   0.05]
lab_u    = ["5/11", "3/11", "3/11",  "3/9",  "2/9",  "4/9",  "3/9",  "2/7",  "3/6",  "3/6",  "1/5",  "1/5"]
# CI half-widths (approximate from visual shading)
err_u_lo = [  0.50,    0.5,   0.55,   0.45,    1.0,    0.7,   0.40,    1.5,   0.88,    2.0,   0.05,   0.05]
err_u_hi = [  0.50,   0.35,   0.35,   0.35,   0.30,   0.42,   0.40,    0.2,   0.05,    0.2,   0.05,   0.05]

x_d      = [     3,      7,     10,     17,     23,     33,     46,     49,     51,     57,     68,     74,     79,     82,     88,     95]
y_d      = [  2.65,   2.72,   2.72,    2.4,   2.45,   1.78,   0.55,   1.78,   1.30,    0.6,   1.15,   1.16,   1.16,   1.14,   1.75,   1.90]
lab_d    = ["7/10", "7/10", "7/10", "6/10",  "6/9",  "4/9",  "2/8",  "4/8",  "3/8",  "2/7",  "3/7",  "3/7",  "3/7",  "3/7",  "4/6",  "4/5"]
err_d_lo = [  0.70,   0.70,   0.70,    0.9,    1.0,   0.70,   0.50,   0.95,   0.45,    3.0,    3.0,    3.0,   3.38,   3.38,    1.0,    1.0]
err_d_hi = [   0.0,    0.0,    0.0,   0.15,    0.1,   0.10,   0.50,   0.20,   0.45,   0.50,    0.4,   0.40,   0.40,   0.38,   0.25,   0.10]

# ── Label offsets: (dy, va) per point ────────────────────────────────────────
# Positive dy = above point, negative = below
OFFS_U = [
    ( 0.12, "bottom"),  # 5/11
    (-0.14, "top"),     # 3/11
    ( 0.12, "bottom"),  # 3/9
    (-0.13, "top"),     # 2/9
    ( 0.12, "bottom"),  # 4/9
    (-0.13, "top"),     # 3/9
    (-0.13, "top"),     # 2/7
    ( 0.12, "bottom"),  # 3/6
    ( 0.12, "bottom"),  # 3/6
    (-0.13, "top"),     # 2/5
    ( 0.12, "bottom"),  # 1/5  (x=55)
    (-0.13, "top"),     # 1/5  (x=60)
]

OFFS_D = [
    (-0.14, "top"),     # 7/10  ← below (x=3)
    ( 0.12, "bottom"),  # 7/10  ← above (x=7, peak)
    (-0.14, "top"),     # 7/10  ← below (x=10)
    ( 0.12, "bottom"),  # 6/10
    ( 0.12, "bottom"),  # 6/9
    (-0.13, "top"),     # 4/9
    (-0.13, "top"),     # 3/9
    ( 0.12, "bottom"),  # 4/8
    (-0.13, "top"),     # 2/7
    (-0.14, "top"),     # 2/8  ← below (x=51, trough)
    ( 0.12, "bottom"),  # 3/8
    (-0.13, "top"),     # 3/6  ← below (x=63, secondary dip)
    ( 0.12, "bottom"),  # 3/7  (x=68, plateau start)
    ( 0.12, "bottom"),  # 3/7
    (-0.13, "top"),     # 3/7
    ( 0.12, "bottom"),  # 3/7
    ( 0.12, "bottom"),  # 4/6
    ( 0.12, "bottom"),  # 4/5
]


def build(out: Path,
          fig_w: float = 3000 / 150,
          fig_h: float = 1000 / 150,
          fs_title: int = 36,
          fs_xlabel: int = 26,
          fs_ylabel: int = 24,
          fs_tick: int = 22,
          fs_label: int = 18,
          fs_legend: int = 22,
          fs_note: int = 17,
          lw_line: float = 3.0,
          ms_marker: float = 9.0,
          ):

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    x_u_arr = np.array(x_u)
    y_u_arr = np.array(y_u)
    lo_u    = np.clip(y_u_arr - err_u_lo, 0, None)
    hi_u    = y_u_arr + err_u_hi

    x_d_arr = np.array(x_d)
    y_d_arr = np.array(y_d)
    lo_d    = np.clip(y_d_arr - err_d_lo, 0, None)
    hi_d    = y_d_arr + err_d_hi

    # Shaded CI bands
    ax.fill_between(x_u_arr, lo_u, hi_u, color=COLOR_U, alpha=0.18, zorder=1)
    ax.fill_between(x_d_arr, lo_d, hi_d, color=COLOR_D, alpha=0.18, zorder=1)

    # Lines + markers
    ax.plot(x_u_arr, y_u_arr, "-o",
            color=COLOR_U, linewidth=lw_line, markersize=ms_marker,
            markerfacecolor=COLOR_U, markeredgecolor=BG, markeredgewidth=1.5,
            label="undirected", zorder=3)
    ax.plot(x_d_arr, y_d_arr, "-o",
            color=COLOR_D, linewidth=lw_line, markersize=ms_marker,
            markerfacecolor=COLOR_D, markeredgecolor=BG, markeredgewidth=1.5,
            label="directed", zorder=3)

    # Data point labels
    for xi, yi, lab, (dy, va) in zip(x_u_arr, y_u_arr, lab_u, OFFS_U):
        ax.text(xi, yi + dy, lab,
                ha="center", va=va,
                fontsize=fs_label, color=COLOR_U, zorder=5)

    for xi, yi, lab, (dy, va) in zip(x_d_arr, y_d_arr, lab_d, OFFS_D):
        ax.text(xi, yi + dy, lab,
                ha="center", va=va,
                fontsize=fs_label, color=COLOR_D, zorder=5)

    # Axes styling
    ax.set_xlim(-2, 102)
    ax.set_ylim(-0.08, 3.10)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="x", labelsize=fs_tick, colors=T_SEC, length=5, width=1.4, pad=8)
    ax.tick_params(axis="y", labelsize=fs_tick, colors=T_SEC, length=5, width=1.4, pad=6)
    ax.set_xlabel("Cumulative hillclimb-hours",
                  fontsize=fs_xlabel, color=T_SEC, labelpad=14)
    ax.set_ylabel("Category entropy\nacross workers (bits)",
                  fontsize=fs_ylabel, color=T_SEC, labelpad=14)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["left"].set_visible(True)
    ax.spines["bottom"].set_visible(True)
    ax.spines["left"].set_color(STROKE_HUD)
    ax.spines["left"].set_linewidth(1.8)
    ax.spines["bottom"].set_color(STROKE_HUD)
    ax.spines["bottom"].set_linewidth(1.8)

    ax.yaxis.grid(True, color=STROKE_HUD, linewidth=0.9,
                  linestyle="--", dashes=(4, 6), alpha=0.5, zorder=0)
    ax.xaxis.grid(True, color=STROKE_HUD, linewidth=0.9,
                  linestyle="--", dashes=(4, 6), alpha=0.5, zorder=0)
    ax.set_axisbelow(True)

    ax.set_title("Entropy collapse of research ideas",
                 fontsize=fs_title, fontweight="bold",
                 color=COLOR_D, pad=18)

    ax.legend(
        loc="lower right",
        fontsize=fs_legend,
        framealpha=0.45,
        facecolor=PANEL,
        edgecolor=STROKE_HUD,
        labelcolor=T_PRI,
        handlelength=2.2,
        handleheight=1.2,
        borderpad=0.9,
        labelspacing=0.5,
        markerscale=1.1,
    )

    ax.text(0.01, 0.06,
            "label = n distinct categories / workers at the iteration",
            transform=ax.transAxes,
            fontsize=fs_note, color=T_MUTED, ha="left", va="bottom", zorder=5)

    fig.tight_layout(pad=1.4)
    fig.savefig(out, dpi=150, bbox_inches="tight",
                facecolor=BG, pad_inches=0.18)
    svg_out = out.with_suffix(".svg")
    fig.savefig(svg_out, format="svg", bbox_inches="tight",
                facecolor=BG, pad_inches=0.18)
    plt.close(fig)
    print(f"Saved → {out}")
    print(f"Saved → {svg_out}")


if __name__ == "__main__":
    # v1 — 3000×1000 px (3:1 ratio), canonical — overwrites main dark png
    build(
        FIGURE_DIR / "paper_fig07_category_entropy_dark.png",
        fig_w=3000 / 150, fig_h=1000 / 150,
        fs_title=36, fs_xlabel=26, fs_ylabel=24,
        fs_tick=22, fs_label=18, fs_legend=22, fs_note=17,
        lw_line=3.0, ms_marker=9.0,
    )

    # v2 — 3000×820 px (3.65:1 ratio), more compressed
    build(
        FIGURE_DIR / "paper_fig07_category_entropy_dark_v2.png",
        fig_w=3000 / 150, fig_h=820 / 150,
        fs_title=34, fs_xlabel=24, fs_ylabel=22,
        fs_tick=20, fs_label=16, fs_legend=20, fs_note=15,
        lw_line=2.8, ms_marker=8.0,
    )
