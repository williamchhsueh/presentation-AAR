"""gen_fig10.py — Two separate dark-theme figures for slide use.

Outputs (v3 quality by default):
  paper_fig10_prescriptive_dark.png   — left panel only
  paper_fig10_autonomous_dark.png     — right panel only
"""
import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── Color tokens ─────────────────────────────────────────────────────────────
BG         = "#081010"
PANEL      = "#101818"
PANEL2     = "#181820"
STROKE_HUD = "#3A4A55"
T_PRI      = "#F8F8F8"
T_SEC      = "#B8C0C4"
T_MUTED    = "#7A8488"
ACCENT_SWE = "#B89AE6"
ACCENT_BLUE= "#3060A0"

FIGURE_DIR = Path(__file__).parent.parent / "figure"


# ── Drawing primitives ────────────────────────────────────────────────────────

def rounded_box(ax, cx, cy, w, h, label, label2=None,
                fc=PANEL, ec=STROKE_HUD, lw=3.0,
                fontsize=18, fontcolor=T_PRI, bold=False,
                ec2=None, lw2=5.0):
    ax.add_patch(FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle="round,pad=0.18",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3,
    ))
    if ec2:
        ax.add_patch(FancyBboxPatch(
            (cx - w/2 - 0.09, cy - h/2 - 0.09), w + 0.18, h + 0.18,
            boxstyle="round,pad=0.27",
            facecolor="none", edgecolor=ec2, linewidth=lw2, alpha=0.50, zorder=2,
        ))
    weight = "bold" if bold else "normal"
    if label2:
        ax.text(cx, cy + 0.20, label, ha="center", va="center",
                fontsize=fontsize, color=fontcolor, fontweight=weight, zorder=5)
        ax.text(cx, cy - 0.35, label2, ha="center", va="center",
                fontsize=fontsize - 4, color=T_SEC, zorder=5)
    else:
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=fontsize, color=fontcolor, fontweight=weight, zorder=5)


def rect_edge(cx, cy, w, h, dx, dy, gap=0.28):
    """Exact edge point of a rectangle in direction (dx,dy) from centre, plus a small gap."""
    ew = w / 2 + gap
    eh = h / 2 + gap
    if abs(dx) < 1e-9:
        return cx, cy + math.copysign(eh, dy)
    if abs(dy) < 1e-9:
        return cx + math.copysign(ew, dx), cy
    t = min(ew / abs(dx), eh / abs(dy))
    return cx + dx * t, cy + dy * t


def solid_arrow(ax, x1, y1, x2, y2, color=T_SEC, lw=4.0, head=0.40):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle=f"-|>,head_width={head},head_length={head*1.15}",
                    color=color, lw=lw,
                    connectionstyle="arc3,rad=0",
                ), zorder=4)


def bidir_dashed(ax, x1, y1, x2, y2, color=T_SEC, lw=3.0, head=0.34):
    """Two overlapping single-direction dashed arrows drawn ABOVE boxes (zorder=5)."""
    kw = dict(color=color, lw=lw, linestyle=(0, (5, 4)),
              connectionstyle="arc3,rad=0")
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle=f"-|>,head_width={head},head_length={head*1.1}", **kw),
                zorder=5)
    ax.annotate("", xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(
                    arrowstyle=f"-|>,head_width={head},head_length={head*1.1}", **kw),
                zorder=5)


# ══════════════════════════════════════════════════════════════════════════════
# Figure A — Prescriptive scaffolding
# ══════════════════════════════════════════════════════════════════════════════

def build_prescriptive(out: Path,
                       fs_title=28, fs_sub=19, fs_box=24, fs_rep=20,
                       lw_box=4.5, lw_arr=4.5, head=0.44,
                       W=8.5, H=13.5, BW=5.8, BH=1.05, GAP=1.82,
                       top_margin=2.55):
    BOX_PAD = 0.18          # must match boxstyle pad= value
    fig = plt.figure(figsize=(W, H), dpi=100, facecolor=BG)
    ax  = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    CX   = W / 2
    steps = ["Propose idea", "Generate plan", "Write code",
             "Smoke tests",  "Full training", "Analyze results"]
    n    = len(steps)
    top  = H - top_margin    # first box centre, clear of subtitle
    ys   = [top - i * GAP for i in range(n)]

    ax.text(CX, H - 0.58, "Prescriptive scaffolding",
            ha="center", va="center", fontsize=fs_title, color=T_PRI,
            fontweight="bold", zorder=5)
    ax.text(CX, H - 1.18, "fixed workflow loop",
            ha="center", va="center", fontsize=fs_sub, color=T_MUTED, zorder=5)

    for label, cy in zip(steps, ys):
        rounded_box(ax, CX, cy, BW, BH, label,
                    ec=STROKE_HUD, lw=lw_box,
                    fontsize=fs_box, fontcolor=ACCENT_SWE)

    # arrows between boxes: start at rendered bottom edge, end at rendered top edge
    # gap = BOX_PAD + tiny buffer so arrowhead is just outside the rendered border
    EDGE_GAP = BOX_PAD + 0.04
    for i in range(n - 1):
        p1x, p1y = rect_edge(CX, ys[i],   BW, BH, 0, -1, gap=EDGE_GAP)
        p2x, p2y = rect_edge(CX, ys[i+1], BW, BH, 0,  1, gap=EDGE_GAP)
        solid_arrow(ax, p1x, p1y, p2x, p2y, color=T_SEC, lw=lw_arr, head=head)

    # repeat loop — attach to rendered left edge of box 1 and box 6
    lx    = CX - BW/2 - BOX_PAD - 0.90
    y_top = ys[0]   + BH/2 + BOX_PAD      # rendered top of first box
    y_bot = ys[n-1] - BH/2 - BOX_PAD      # rendered bottom of last box
    entry_x = CX - BW/2 - BOX_PAD - 0.05  # just left of rendered box edge
    ax.annotate("", xy=(entry_x, y_top),
                xytext=(lx, y_top),
                arrowprops=dict(
                    arrowstyle=f"-|>,head_width={head+0.02},head_length={(head+0.02)*1.15}",
                    color=T_SEC, lw=lw_arr,
                    connectionstyle="arc3,rad=0"), zorder=5)
    ax.plot([lx, lx], [y_bot, y_top], color=T_SEC, lw=lw_arr, zorder=5)
    ax.plot([entry_x, lx], [y_bot, y_bot], color=T_SEC, lw=lw_arr, zorder=5)
    ax.text(lx - 0.52, (y_bot + y_top) / 2, "repeat",
            ha="center", va="center", fontsize=fs_rep, color=T_SEC,
            rotation=90, zorder=5)

    fig.savefig(out, dpi=100, bbox_inches="tight", facecolor=BG, pad_inches=0.20)
    plt.close(fig)
    print(f"Saved → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Figure B — Autonomous scaffolding
# ══════════════════════════════════════════════════════════════════════════════

def build_autonomous(out: Path,
                     fs_title=28, fs_sub=19, fs_hub=26, fs_node=21,
                     lw_box_hub=5.0, lw_box_node=3.8, lw_arr=3.2, head=0.36):
    BOX_PAD = 0.18          # must match boxstyle pad= value
    W, H = 12.0, 11.5
    fig = plt.figure(figsize=(W, H), dpi=100, facecolor=BG)
    ax  = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    RX, RY  = W / 2, H / 2 - 0.4
    HW, HH  = 4.2, 1.55
    NW, NH  = 3.0, 0.92
    R_orbit = 3.75

    ax.text(RX, H - 0.58, "Autonomous scaffolding",
            ha="center", va="center", fontsize=fs_title, color=T_PRI,
            fontweight="bold", zorder=5)
    ax.text(RX, H - 1.18, "free-form  ·  any step any time",
            ha="center", va="center", fontsize=fs_sub, color=T_MUTED, zorder=5)

    outer_nodes = [
        ("hypothesize",    122), ("de-risk expt",    58),  # spread wider to avoid overlap
        ("write code",     162), ("analyze data",    18),
        ("full training",  198), ("tune hparams",   342),
        ("ablate",         228), ("share findings", 312),
    ]
    node_pos = {}
    for label, angle in outer_nodes:
        rad = math.radians(angle)
        node_pos[label] = (RX + R_orbit * math.cos(rad),
                           RY + R_orbit * math.sin(rad))

    # Strategy:
    #   arrows zorder=4  →  drawn between box fill (3) and box edges+text (5)
    #   boxes  zorder=3 fill, zorder=6 for their EDGE STROKE redraw to cover
    #          any arrowhead that bleeds onto the box border
    #   We clip each arrow to start/end exactly at the rendered box edge
    #   (gap = BOX_PAD so we land right on the rendered edge, not inside it)

    for label, (nx, ny) in node_pos.items():
        dx, dy = nx - RX, ny - RY
        # gap = BOX_PAD positions the arrowhead exactly at the rendered box edge
        hx, hy = rect_edge(RX, RY, HW, HH, dx,   dy,  gap=BOX_PAD + 0.04)
        ex, ey = rect_edge(nx, ny, NW, NH, -dx, -dy,  gap=BOX_PAD + 0.04)
        bidir_dashed(ax, hx, hy, ex, ey, color=T_SEC, lw=lw_arr, head=head)

    # Draw hub — zorder=3 fill covers arrow line inside; redraw edge at zorder=6
    rounded_box(ax, RX, RY, HW, HH, "AAR", "decides next step",
                fc=PANEL2, ec=ACCENT_BLUE, lw=lw_box_hub,
                fontsize=fs_hub, fontcolor=ACCENT_SWE, bold=True,
                ec2=ACCENT_BLUE, lw2=lw_box_hub + 1.5)
    # overlay stroke only (no fill) on top of arrows so arrowheads at hub edge are clean
    ax.add_patch(FancyBboxPatch(
        (RX - HW/2, RY - HH/2), HW, HH,
        boxstyle=f"round,pad={BOX_PAD}",
        facecolor="none", edgecolor=ACCENT_BLUE, linewidth=lw_box_hub, zorder=6,
    ))

    # Draw outer nodes — same overlay trick
    for label, (nx, ny) in node_pos.items():
        rounded_box(ax, nx, ny, NW, NH, label,
                    ec=STROKE_HUD, lw=lw_box_node,
                    fontsize=fs_node, fontcolor=T_PRI)
        ax.add_patch(FancyBboxPatch(
            (nx - NW/2, ny - NH/2), NW, NH,
            boxstyle=f"round,pad={BOX_PAD}",
            facecolor="none", edgecolor=STROKE_HUD, linewidth=lw_box_node, zorder=6,
        ))

    fig.savefig(out, dpi=100, bbox_inches="tight", facecolor=BG, pad_inches=0.20)
    plt.close(fig)
    print(f"Saved → {out}")


# ── Generate ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Original portrait (H/W ≈ 1.59)
    build_prescriptive(
        FIGURE_DIR / "paper_fig10_prescriptive_dark.png")

    # Wide / near-square variant (H/W ≈ 1.09)
    build_prescriptive(
        FIGURE_DIR / "paper_fig10_prescriptive_dark_wide.png",
        fs_title=30, fs_sub=21, fs_box=26, fs_rep=22,
        lw_box=5.0, lw_arr=5.0, head=0.48,
        W=11, H=12, BW=7.0, BH=1.05, GAP=1.72, top_margin=2.4)

    # Landscape variant (H/W ≈ 0.88)
    build_prescriptive(
        FIGURE_DIR / "paper_fig10_prescriptive_dark_landscape.png",
        fs_title=32, fs_sub=22, fs_box=28, fs_rep=24,
        lw_box=5.5, lw_arr=5.5, head=0.52,
        W=13, H=11.5, BW=9.0, BH=1.0, GAP=1.64, top_margin=2.2)

    build_autonomous(
        FIGURE_DIR / "paper_fig10_autonomous_dark.png")

    print("Done.")
