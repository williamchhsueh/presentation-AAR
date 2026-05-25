"""gen_fig09.py — Recreate paper_fig09_AAR_ideas_transfer_dark.png with dark theme.

Generates two variants:
  v1  — canonical (saved over the main _dark.png)
  v2  — slightly taller bars, different palette accent

Usage:
  poetry run python code/gen_fig09.py
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Color tokens (vis_style.md §4) ──────────────────────────────────────────
BG         = "#081010"
PANEL      = "#101818"
STROKE_HUD = "#3A4A55"
T_PRI      = "#F8F8F8"
T_SEC      = "#B8C0C4"
T_MUTED    = "#7A8488"

FIGURE_DIR = Path(__file__).parent.parent / "figure"

# ── Data ────────────────────────────────────────────────────────────────────
categories = ["Chat\n(origin)", "Math", "Code"]
ccs_vals   = [0.97,  0.94,  0.47]
em_vals    = [0.78,  0.75, -0.12]
human_base = [0.25,  0.58,  0.19]

ccs_err = [0.01, 0.01, 0.02]
em_err  = [0.02, 0.02, 0.02]


def build(out: Path,
          color_ccs: str  = "#E85555",
          color_em:  str  = "#5590D0",
          color_base: str = "#C8D0D4",
          # canvas — lower aspect ratio means shorter height
          fig_w: float = 3000 / 150,
          fig_h: float = 1200 / 150,
          # text sizes
          fs_title: int  = 34,
          fs_xtick: int  = 26,
          fs_ytick: int  = 22,
          fs_ylabel: int = 24,
          fs_val:   int  = 22,
          fs_leg:   int  = 22,
          # bar geometry
          bar_w: float = 0.36,
          gap:   float = 0.06,
          ):

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    n       = len(categories)
    x       = np.arange(n)
    offsets = np.array([-bar_w / 2 - gap / 2, bar_w / 2 + gap / 2])

    for i, (vals, err, color, label) in enumerate([
        (ccs_vals, ccs_err, color_ccs, "CCS + Self-Distill"),
        (em_vals,  em_err,  color_em,  "EM Posterior"),
    ]):
        bars = ax.bar(
            x + offsets[i], vals,
            width=bar_w, color=color,
            linewidth=0, zorder=3, label=label,
        )
        for bar, v in zip(bars, vals):
            dy = 0.022 if v >= 0 else -0.022
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                v + dy,
                f"{v:.2f}",
                ha="center",
                va="bottom" if v >= 0 else "top",
                fontsize=fs_val, fontweight="bold",
                color=T_PRI, zorder=5,
            )
        ax.errorbar(
            x + offsets[i], vals, yerr=err,
            fmt="none", ecolor=T_PRI,
            elinewidth=2.5, capsize=7, capthick=2.5, zorder=4,
        )

    # Per-category human-tuned baselines
    for xi, hv in zip(x, human_base):
        ax.hlines(
            hv,
            xi - bar_w - gap / 2 - 0.06,
            xi + bar_w + gap / 2 + 0.06,
            colors=color_base, linewidths=4.0,
            linestyles=(0, (4, 2)), zorder=5,
        )

    # Axes
    ax.set_xlim(-0.65, n - 0.35)
    ax.set_ylim(-0.30, 1.14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=fs_xtick, color=T_SEC)
    ax.tick_params(axis="x", length=0, pad=10)
    ax.set_ylabel("PGR", fontsize=fs_ylabel, color=T_SEC, labelpad=14)
    ax.tick_params(axis="y", labelsize=fs_ytick, colors=T_SEC, length=4, width=1.4)

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
    ax.set_axisbelow(True)
    ax.axhline(0, color=STROKE_HUD, linewidth=1.8, zorder=2)

    ax.set_title(
        "Do AAR-discovered ideas transfer to held-out datasets?",
        fontsize=fs_title, fontweight="bold",
        color=color_ccs, pad=20,
    )

    legend_handles = [
        mpatches.Patch(facecolor=color_ccs, label="CCS + Self-Distill"),
        mpatches.Patch(facecolor=color_em,  label="EM Posterior"),
        plt.Line2D([0], [0], color=color_base, linewidth=4.0,
                   linestyle=(0, (4, 2)), label="Human-tuned"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        fontsize=fs_leg,
        framealpha=0.88,
        facecolor=PANEL,
        edgecolor=STROKE_HUD,
        labelcolor=T_PRI,
        handlelength=2.4,
        handleheight=1.5,
        borderpad=1.0,
        labelspacing=0.6,
    )

    fig.tight_layout(pad=1.6)
    fig.savefig(out, dpi=150, bbox_inches="tight",
                facecolor=BG, pad_inches=0.18)
    # also save SVG alongside the PNG
    svg_out = out.with_suffix(".svg")
    fig.savefig(svg_out, format="svg", bbox_inches="tight",
                facecolor=BG, pad_inches=0.18)
    plt.close(fig)
    print(f"Saved → {out}")
    print(f"Saved → {svg_out}")


if __name__ == "__main__":
    # v1 — warm crimson / steel blue  (canonical, overwrites main dark png)
    build(
        FIGURE_DIR / "paper_fig09_AAR_ideas_transfer_dark.png",
        color_ccs="#E85555", color_em="#5590D0",
    )

    # v2 — amber / violet palette  (alternate accent)
    build(
        FIGURE_DIR / "paper_fig09_AAR_ideas_transfer_dark_v2.png",
        color_ccs="#E8963A", color_em="#8B6DD4",
        fs_title=34, fs_xtick=26, fs_ytick=22, fs_ylabel=24,
        fs_val=22, fs_leg=22,
    )
